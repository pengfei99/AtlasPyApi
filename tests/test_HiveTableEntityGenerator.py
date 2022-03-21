import json

from atlas_client.entity_source_generation.HiveTableEntityGenerator import HiveTableEntityGenerator


def test_generate_hive_table_json_source():
    generated_json_str = HiveTableEntityGenerator. \
        generate_hive_table_json_source("students", "insee.fr@insee-data", 'this table describes students information')

    expected_result = {
        "referredEntities": {},
        "entity": {
            "typeName": "hive_table",
            "attributes": {
                "owner": "null",
                "temporary": "false",
                "aliases": [],
                "replicatedTo": [],
                "replicatedFrom": [],
                "qualifiedName": "insee.fr@insee-data.students",
                "displayName": "students",
                "description": "this table describes students information",
                "db": {
                    "typeName": "hive_db",
                    "uniqueAttributes": {
                        "qualifiedName": "insee.fr@insee-data"
                    }
                },
                "name": "students",
                "retention": 0
            },
            "isIncomplete": "false",
            "status": "ACTIVE",
            "createdBy": "hive_hook",
            "updatedBy": "hive_hook",
            "version": 0,
            "labels": []
        }
    }
    # we need to remove the timestamp, because it uses current time each time, test will not pass
    generated_result = json.loads(generated_json_str)
    print(generated_result)
    del generated_result["entity"]["attributes"]["lastAccessTime"]
    del generated_result["entity"]["attributes"]["createTime"]
    del generated_result["entity"]["createTime"]
    del generated_result["entity"]["updateTime"]
    assert generated_result == expected_result
