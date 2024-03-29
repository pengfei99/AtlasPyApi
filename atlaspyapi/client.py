#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import copy
import functools
import io
import json
import tarfile
from typing import List

import requests

from atlaspyapi import models, utils, base, exceptions
from atlaspyapi.exceptions import handle_response, BadHttpAuthArg
from atlaspyapi.log_manager import LogManager

LOG = LogManager(__name__).get_logger()

# this defines where the Atlas client delegates to for actual logic
ENTRY_POINTS = {
    "entity_guid": models.EntityGuid,
    "typedefs": models.TypeDef,
    "entity_post": models.EntityPost,
    "entity_bulk": models.EntityBulk,
    "entity_bulk_classification": models.EntityBulkClassification,
    "entity_unique_attribute": models.EntityUniqueAttribute,
    "typedefs_headers": models.TypeDefHeader,
    "classificationdef_guid": models.ClassificationDefGuid,
    "classificationdef_name": models.ClassificationDefName,
    "entitydef_guid": models.EntityDefGuid,
    "entitydef_name": models.EntityDefName,
    "enumdef_guid": models.EnumDefGuid,
    "enumdef_name": models.EnumDefName,
    "relationshipdef_guid": models.RelationshipDefGuid,
    "relationshipdef_name": models.RelationshipDefName,
    "structdef_guid": models.StructDefGuid,
    "structdef_name": models.StructDefName,
    "typedef_guid": models.TypeDefGuid,
    "typedef_name": models.TypeDefName,
    "lineage_guid": models.LineageGuid,
    "search_attribute": models.SearchAttribute,
    "search_basic": models.SearchBasic,
    "search_dsl": models.SearchDsl,
    "search_fulltext": models.SearchFulltext,
    "relationship": models.Relationship,
    "relationship_guid": models.RelationshipGuid,
    "search_saved": models.SearchSaved,
    "admin_metrics": models.AdminMetrics,
}


class Atlas(object):
    """The Atlas client

    This is the entry point to the Atlas API. Create this client and then
    use one of the entry points to start hitting Atlas object collections.
    """

    def __init__(
            self,
            host: str,
            port: int = None,
            username: str = None,
            password: str = None,
            oidc_token: str = None,
            identifier: str = None,
            protocol: str = None,
            validate_ssl: bool = True,
            timeout=10,
            max_retries=5,
            auth=None,
    ):
        self.oidc_token = oidc_token
        self.base_url = utils.generate_base_url(host, port=port, protocol=protocol)
        if identifier is None:
            identifier = "python-atlasclient"
        self.client = HttpClient(
            host=self.base_url,
            username=username,
            password=password,
            identifier=identifier,
            oidc_token=oidc_token,
            validate_ssl=validate_ssl,
            timeout=timeout,
            max_retries=max_retries,
            auth=auth,
        )

        self._version = None

    def __dir__(self):
        d1 = {}
        d1.update(self.__dict__)
        d1.update(ENTRY_POINTS)
        return d1.keys()

    def check_version(self):
        if self.version < base.OLDEST_SUPPORTED_VERSION:
            raise exceptions.ClientError(
                "Version %s unsupported, must be %s or higher"
                % (
                    utils.version_str(self.version),
                    utils.version_str(base.OLDEST_SUPPORTED_VERSION),
                )
            )
        return

    def __getattr__(self, attr):
        if attr in ENTRY_POINTS:
            rel_class = ENTRY_POINTS[attr]
            return rel_class.collection_class(self, rel_class)

        if getattr(requests, attr):
            # forward get/post/put/head/delete to the http client
            return getattr(self.client, attr)

        raise AttributeError(attr)

    def purge_entity_by_guid(self, guids: List[str]):
        """
        This method takes a list of GUIDs for Atlas entities, each entity in the list is purged from Atlas if the
        entity is already marked as deleted. This call requires a user account with Atlas administrator privileges.
        The successfully purged entities are listed in the audit log, referenced by their GUIDs.

        param guids: The list of guids which we want to delete
        """
        LOG.debug("Call purge entity by guid")
        headers = {
            "Authorization": self.client.auth_header,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        purge_url = f"{self.base_url}/api/atlas/admin/purge/"
        response = requests.put(purge_url, data=json.dumps(guids), headers=headers)
        LOG.debug(f"Purge request response: {response}")
        return response

    def get_guid_by_qualified_name(
            self, entity_type_name: str, entity_qualified_name, **kwargs
    ):
        if "limit" in kwargs and isinstance(kwargs["limit"], int):
            input_limit = kwargs["limit"]
        else:
            input_limit = 10
        if "offset" in kwargs and isinstance(kwargs["offset"], int):
            input_offset = kwargs["offset"]
        else:
            input_offset = 0
        headers = {
            "Authorization": self.client.auth_header,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        params = {
            "attrName": "qualifiedName",
            "attrValuePrefix": f"{entity_qualified_name}",
            "limit": f"{input_limit}",
            "offset": f"{input_offset}",
            "typeName": f"{entity_type_name}",
        }
        search_url = f"{self.base_url}/api/atlas/v2/search/attribute"
        response = requests.get(f"{search_url}", params=params, headers=headers)
        # convert response json text to python dict
        response_dict = json.loads(response.text)
        LOG.debug(f"Response dict : {response_dict}")
        guid = None
        try:
            guid = response_dict.get("entities")[0].get("guid")
            LOG.debug("Extract the first guid:{guid} ")
        except Exception as e:
            LOG.exception(f"Entity that you are looking for does not exist. {e}")
        return guid


class HttpClient(object):
    """Our HTTP based REST client.

    It handles some of the dirty work like automatic serialization/deserialization
    of JSON data, converting error responses to exceptions, etc.  For the most
    part it should mimic a requests client. You can call methods like get, post,
    put, delete, and head and expect them to work the same way.  But instead of
    a response object, you get a dictionary.  A response of None means no response
    was supplied by the API.  This should be uncommon except for error cases, but
    cases do exist either due to Atlas bugs or other mitigating circumstances.
    """

    def __init__(
            self,
            host,
            identifier,
            username=None,
            password=None,
            oidc_token=None,
            validate_ssl=True,
            timeout=10,
            max_retries=5,
            auth=None,
    ):
        if oidc_token:
            self.auth_header = f"Bearer {oidc_token}"
        elif username and password:
            basic_token = utils.generate_http_basic_token(
                username=username, password=password
            )
            self.auth_header = f"Basic {basic_token}"
        else:
            raise BadHttpAuthArg
        self.request_params = {
            "headers": {
                "X-Requested-By": identifier,
                "Authorization": self.auth_header,
            },
            "verify": validate_ssl,
            "timeout": timeout,
        }
        # automatically retry requests on connection errors
        self.session = requests.Session()
        self.session.auth = auth
        adapter = requests.adapters.HTTPAdapter(max_retries=max_retries)
        self.session.mount(host, adapter)

    def request(self, method, url, content_type=None, **kwargs):
        # doing it this way keeps the magic for following redirects intact
        requests_method = getattr(self.session, method)
        params = copy.deepcopy(self.request_params)
        params.update(kwargs)

        if content_type is not None:
            params["headers"]["Content-type"] = content_type
        else:
            params["headers"]["Content-type"] = "application/json"
        LOG.debug("Request headers: %s", params["headers"])

        if "data" in params and isinstance(params["data"], dict):
            params["data"] = json.dumps(params["data"], cls=AtlasJsonEncoder)
            LOG.debug("Request body: %s", params["data"])
        elif "data" in params and isinstance(params["data"], str):
            params["data"] = json.dumps(params["data"])
        elif "data" in params and isinstance(params["data"], list):
            params["data"] = json.dumps(params["data"])

        LOG.debug(f"Requesting Atlas with the '{method}' method.")
        if params.get("data"):
            LOG.debug(f"With the following data: {params['data']}")

        response = requests_method(url, **params)

        # any error responses will generate exceptions here
        handle_response(response)

        LOG.debug("Response headers: %s", response.headers)
        if response.status_code != 204 and len(response.content):
            LOG.debug("Response: %s", response.json())

        if response.headers.get("content-length") is None:
            # Log bad methods so we can report them
            LOG.debug(
                "Missing content-length for %s %s: %s",
                method,
                url,
                response.headers.get("content-type"),
            )

        # there is no consistent way to determine response type
        # so assume json if it's not an empty string
        if response.text:
            if response.headers.get("content-type") == "application/x-ustar":
                tarstream = io.BytesIO(response.content)
                tarstream.seek(0)
                return tarfile.open(fileobj=tarstream)
            elif "application/json" not in response.headers.get("content-type"):
                # Log bad methods so we can report them
                LOG.debug(
                    "Wrong response content-type for %s %s: %s",
                    method,
                    url,
                    response.headers.get("content-type"),
                )
            return response.json()

        return {}

    def __getattr__(self, attr):
        if getattr(requests, attr):
            return functools.partial(self.request, attr)
        raise AttributeError(attr)


class AtlasJsonEncoder(json.JSONEncoder):
    """Converts Atlas model objects into dictionaries that can be JSON-encoded

    This allows for passing in models and ModelCollections into related objects'
    create/update methods and having it handle the conversion automatically.
    """

    def default(self, obj):  # pylint: disable=method-hidden
        if isinstance(obj, base.ModelCollection):
            dicts = []
            for model in obj:
                dicts.append(model.to_json_dict())
            return dicts
        elif isinstance(obj, base.Model):
            return obj.to_json_dict()
        # Let the base class default method raise the TypeError
        return super(AtlasJsonEncoder, self).default(obj)
