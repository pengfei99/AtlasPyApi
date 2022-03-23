from atlas_client.client import Atlas
from atlas_client.entity_search.EntityFinder import EntityFinder
from my_secrets import secret


def main():
    local = False
    # config for atlas client
    atlas_prod_hostname = "https://atlas.lab.sspcloud.fr"
    atlas_prod_port = 443
    oidc_token = secret.oidc_token
    atlas_local_hostname = "http://localhost"
    login = "admin"
    pwd = "admin"

    if local:
        atlas_client = Atlas(atlas_local_hostname, port=21000, username=login, password=pwd)
    else:
        # create an instance of the atlas Client with oidc token
        atlas_client = Atlas(atlas_prod_hostname, atlas_prod_port, oidc_token=oidc_token)
    entity_finder = EntityFinder(atlas_client)
    res = entity_finder.search_full_text("hive_table", "user-pengfei@movies.Character")
    EntityFinder.show_search_results(res)
    guids = EntityFinder.get_result_entity_guid_list(res)
    print(guids)


if __name__ == "__main__":
    main()
