from atlaspyapi.client import Atlas
from atlaspyapi.entity_search.EntityFinder import EntityFinder
from my_secrets import secret


def full_text_search_test(entity_finder):
    type_name = "hive_table"
    qualified_name = "user-tm8enk@default.sirene"
    res = entity_finder.search_full_text(type_name, qualified_name)
    EntityFinder.show_search_results(res)
    guids = EntityFinder.get_result_entity_guid_list(res)
    print(f"full text search result: {guids}")


def get_guid_by_qualified_name_test(entity_finder):
    type_name = "hive_table"
    qualified_name = "user-tm8enk@default.individu_reg"
    res1 = entity_finder.get_guid_by_qualified_name(type_name, qualified_name)
    print(f"qualified name search result: {res1}")


def main():
    """
    This script tests the two method of the EntityFinder
    - search_full_text
    - get_guid_by_qualified_name

    As we don't find a way to mock Atlas server in github, so we exclude these tests from the pytest framework.
    Otherwise, the github ci will fail
    """
    local = False
    # config for atlas client

    if local:
        atlas_local_hostname = "http://localhost"
        login = "admin"
        pwd = "admin"
        atlas_client = Atlas(atlas_local_hostname, port=21000, username=login, password=pwd)
    else:
        # create an instance of the atlas Client with oidc token
        atlas_prod_hostname = "https://atlas.lab.sspcloud.fr"
        atlas_prod_port = 443
        oidc_token = secret.oidc_token
        atlas_client = Atlas(atlas_prod_hostname, atlas_prod_port, oidc_token=oidc_token)
    entity_finder = EntityFinder(atlas_client)
    # full_text_search_test(entity_finder)
    get_guid_by_qualified_name_test(entity_finder)


if __name__ == "__main__":
    main()
