from atlas_client.client import Atlas
from atlas_client.entity_search.EntityFinder import EntityFinder
from my_secrets import secret


def main():
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
    t_guid = entity_finder.get_guid_by_qualified_name("hive_table", "default.students")
    print(t_guid)
    d_guid = entity_finder.get_guid_by_qualified_name("hive_db", "default")
    print(d_guid)


if __name__ == "__main__":
    main()
