import json

from atlaspyapi.entity_source_generation.HiveColumnEntityGenerator import HiveColumnEntityGenerator


def test_generate_hive_column_json_source():
    generated_json_str = HiveColumnEntityGenerator. \
        generate_hive_column_json_source("studentId", "int", "insee.fr@insee-data.students",
                                         'this column describes the students ID')

    expected_result = {
        "referredEntities": {},
        "entity": {
            "typeName": "hive_column",
            "attributes": {
                "owner": "null",
                "replicatedTo": [],
                "replicatedFrom": [],
                "qualifiedName": "insee.fr@insee-data.students.studentId",
                "displayName": "studentId",
                "name": "studentId",
                "description": "this column describes the students ID",
                "table": {
                    "typeName": "hive_table",
                    "uniqueAttributes": {
                        "qualifiedName": "insee.fr@insee-data.students"
                    }
                },
                "position": 0,
                "type": "int"
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

    del generated_result["entity"]["createTime"]
    del generated_result["entity"]["updateTime"]
    assert generated_result == expected_result
