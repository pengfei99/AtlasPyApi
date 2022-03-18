from atlas_client.client import Atlas
from atlas_client.entity_management.hive.HiveDBManager import HiveDBManager
from atlas_client.entity_management.hive.HiveTableManager import HiveTableManager
from atlas_client.entity_management.hive.HiveColumnManager import HiveColumnManager
from atlas_client.entity_search.EntityFinder import EntityFinder


def main():
    # config for atlas client
    atlas_prod_hostname = "https://atlas.lab.sspcloud.fr"
    atlas_prod_port = 443
    oidc_token = ""
    atlas_local_hostname = "http://localhost"
    login = "admin"
    pwd = "admin"
    # create an instance of the atlas Client with oidc token
    # atlas_prod_client = Atlas(atlas_prod_hostname, atlas_prod_port, oidc_token=oidc_token)
    atlas_local_client = Atlas(atlas_local_hostname, port=21000, username=login, password=pwd)
    finder = EntityFinder(atlas_local_client)
    res = finder.search_full_text("hive_table","pengfei")
    print(f"Search result is {res}")
    hive_db = HiveDBManager(atlas_local_client)
    hive_table = HiveTableManager(atlas_local_client)
    hive_column = HiveColumnManager(atlas_local_client)

    # insert hive tables
    hive_db.create_entity("pengfei-stock", "pengfei.org", "database for my stock market")
    hive_table.create_entity("favorite", "pengfei.org@pengfei-stock", "favorite stock")
    hive_column.create_entity("stock_id", "int", "pengfei.org@pengfei-stock.favorite", "id of the stock")
    hive_column.create_entity("stock_name", "string", "pengfei.org@pengfei-stock.favorite", "name of the stock")


if __name__ == "__main__":
    main()
