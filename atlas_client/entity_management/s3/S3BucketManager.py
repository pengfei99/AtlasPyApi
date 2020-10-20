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

import json
from atlas_client.client import Atlas
from atlas_client.definition import TARGET_FOLDER
from atlas_client.entity_management.EntityManager import EntityManager
from atlas_client.entity_source_generation.S3BucketEntityGenerator import S3BucketEntityGenerator


class S3BucketManager(EntityManager):
    def __init__(self, atlas_client: Atlas):
        super().__init__(atlas_client)

    def create_entity(self, name: str, domain: str, qualified_name: str, description: str, **kwargs) -> None:
        s3_bucket_json_source = S3BucketEntityGenerator.generate_s3_bucket_json_source(name, domain, qualified_name,
                                                                                       description, **kwargs)
        target_file = TARGET_FOLDER + "/s3_bucket.json"
        f = open(target_file, "w")
        f.write(s3_bucket_json_source)
        f.close()
        with open(target_file, "r") as json_file:
            s3_bucket_json_source = json.load(json_file)
            print(s3_bucket_json_source)
        try:
            self.client.entity_post.create(data=s3_bucket_json_source)
        except Exception as e:
            print("atlas bucket entity creation failed. Origin exception: " + str(e))
            return False
        else:
            return True
