from atlaspyapi.client import Atlas
from atlaspyapi.entity_management.hive.HiveColumnManager import HiveColumnManager
from atlaspyapi.entity_management.hive.HiveDBManager import HiveDBManager
from atlaspyapi.entity_management.hive.HiveTableManager import HiveTableManager
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
    # finder = EntityFinder(atlaspyapi)
    # res = finder.search_full_text("hive_table", "pengfei")
    # print(f"Search result is {res}")
    hive_db = HiveDBManager(atlas_client)
    hive_table = HiveTableManager(atlas_client)
    # hive_column = HiveColumnManager(atlaspyapi)

    # insert hive tables
    # hive_db.create_entity("pengfei-stock", "pengfei.org", "database for my stock market",owner="pliu",location="pengfei.org")
    # hive_table.create_entity("favorite", "pengfei.org@pengfei-stock", "favorite stock")
    # hive_column.create_entity("stock_id", "int", "pengfei.org@pengfei-stock.favorite", "id of the stock")
    # hive_column.create_entity("stock_name", "string", "pengfei.org@pengfei-stock.favorite", "name of the stock")
    hive_table.delete_entity("e57ce313-ef6c-4ada-b40d-697b693893f6")
    db_guid = "a5201924-87f7-4c3c-aab4-b8086917b108"
    hive_db.delete_entity(db_guid)
    hive_db.purge_entity(db_guid)


if __name__ == "__main__":
    main()
