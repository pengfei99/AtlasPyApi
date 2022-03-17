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
from atlas_client.entity_management.EntityManager import EntityManager
from atlas_client.entity_source_generation.HiveDBEntityGenerator import HiveDBEntityGenerator
from atlas_client.entity_source_generation.HiveTableEntityGenerator import HiveTableEntityGenerator
from atlas_client.log_manager import get_logger

my_logger = get_logger(__name__)
my_logger.debug("a debug message")


class HiveTableManager(EntityManager):
    def __init__(self, atlas_client: Atlas):
        super().__init__(atlas_client)

    def create_entity(self, table_name: str, db_qualified_name: str, description: str, **kwargs) -> bool:
        hive_db_json_source = HiveTableEntityGenerator.generate_hive_table_json_source(table_name, db_qualified_name,
                                                                                       description, **kwargs)

        hive_db_json_source = json.loads(hive_db_json_source)
        try:
            self.client.entity_post.create(data=hive_db_json_source)
        except Exception as e:
            my_logger.error(f"Hive table entity {table_name} creation failed. {e}")
            return False
        else:
            my_logger.info(f"Hive table entity {table_name} is created in db {db_qualified_name}")
            return True
