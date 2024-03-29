from atlaspyapi.client import Atlas
from atlaspyapi.entity_management.hive.HiveColumnManager import HiveColumnManager
from atlaspyapi.entity_management.hive.HiveDBManager import HiveDBManager
from atlaspyapi.entity_management.hive.HiveTableManager import HiveTableManager
from my_secrets import secret


def hive_db_creation_test(hive_db):
    hive_db.create_entity("stock", "user-pengfei", "database for my stock market", owner="pliu",
                          location="pengfei.org")


def hive_db_deletion_test(hive_db):
    db_guid = "a5201924-87f7-4c3c-aab4-b8086917b108"
    hive_db.delete_entity(db_guid)


def hive_db_purge_test(hive_db):
    db_guid = "70a3a0cc-aa34-4df0-800f-2560b02e6e38"
    hive_db.purge_entity(db_guid)


def hive_table_creation_test(hive_table):
    hive_table.create_entity("favorite", "user-pengfei@stock", "favorite stock")


def hive_table_deletion_test(hive_table):
    db_guid = "893f55d2-ffe2-4340-a2a0-262da533ae9a"
    hive_table.delete_entity(db_guid)


def hive_table_purge_test(hive_table):
    db_guid = "a12d1fb7-b8bd-45e9-82d3-6ed222a1146f"
    hive_table.purge_entity(db_guid)


def hive_column_creation_test(hive_column):
    hive_column.create_entity("stock_id", "int", "pengfei.org@pengfei-stock.favorite", "id of the stock")
    hive_column.create_entity("stock_name", "string", "pengfei.org@pengfei-stock.favorite", "name of the stock")


def hive_column_deletion_test(hive_column):
    db_guid = "a5201924-87f7-4c3c-aab4-b8086917b108"
    hive_column.delete_entity(db_guid)


def hive_column_purge_test(hive_column):
    db_guid = "5d1315f2-cee8-4dd0-a2ee-da67139b646e"
    hive_column.purge_entity(db_guid)


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
    hive_db = HiveDBManager(atlas_client)
    hive_table = HiveTableManager(atlas_client)
    hive_column = HiveColumnManager(atlas_client)

    # test hive db operation
    hive_db_creation_test(hive_db)
    # hive_db_deletion_test(hive_db)
    # hive_db_purge_test(hive_db)

    # test hive table operation
    hive_table_creation_test(hive_table)
    # hive_table_deletion_test(hive_table)
    # hive_table_purge_test(hive_table)

    # test hive column operation
    # hive_column_creation_test(hive_column)
    # hive_column_deletion_test(hive_column)
    # hive_column_purge_test(hive_column)


if __name__ == "__main__":
    main()
