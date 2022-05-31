import json

from atlaspyapi.entity_source_generation.HiveDBEntityGenerator import HiveDBEntityGenerator


def test_generate_hive_db_json_source():
    generated_json_str = HiveDBEntityGenerator.generate_hive_db_json_source("insee-data", "insee.fr", "this is a test",
                                                                            owner="admin")

    expected_result = {'referredEntities': {},
                       'entity': {'typeName': 'hive_db',
                                  'attributes': {'owner': 'admin', 'ownerType': 'user',
                                                 'replicatedTo': [], 'replicatedFrom': [],
                                                 'qualifiedName': 'insee.fr@insee-data',
                                                 'displayName': 'insee-data',
                                                 'clusterName': 'insee.fr',
                                                 'name': 'insee-data',
                                                 'description': 'this is a test',
                                                 'location': 'None', 'parameters': None},
                                  'isIncomplete': False, 'status': 'ACTIVE',
                                  'createdBy': 'hive_hook', 'updatedBy': 'hive_hook',
                                  'version': 0, 'labels': []}}
    # we need to remove the timestamp, because it uses current time each time, test will not pass
    generated_result = json.loads(generated_json_str)
    del generated_result["entity"]["createTime"]
    del generated_result["entity"]["updateTime"]
    assert generated_result == expected_result
