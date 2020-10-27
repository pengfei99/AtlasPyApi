from atlas_client.client import Atlas
from atlas_client.entity_management.s3.S3BucketManager import S3BucketManager
from atlas_client.entity_management.s3.S3ObjectManager import S3ObjectManager
from atlas_client.entity_management.s3.S3PsDirManager import S3PsDirManager

hostname = "https://atlas.lab.sspcloud.fr"
port = 443
oidc_token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhUHNCSzhYRC1od1gtMWJFbjdZZDRLS0tWS0hYRy03RHg3STZDaVZZ" \
             "WUtRIn0.eyJleHAiOjE2MDM4Mjk2MDEsImlhdCI6MTYwMzc4NjQwMSwiYXV0aF90aW1lIjoxNjAzNzg2NDAxLCJqdGkiOiI3NDRk" \
             "MTczNy01OTEzLTRiNjgtODI1NC05ZWJhOTNmODY4NGMiLCJpc3MiOiJodHRwczovL2F1dGgubGFiLnNzcGNsb3VkLmZyL2F1dGgvcmV" \
             "hbG1zL3NzcGNsb3VkIiwiYXVkIjpbIm9ueXhpYSIsImFjY291bnQiXSwic3ViIjoiNDczNDkxMjgtNGE0Yy00MjI2LWE1YjEtNjgwOD" \
             "AxYWY1YTJiIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoib255eGlhIiwibm9uY2UiOiI1YjZlYzdlNy1jNjA5LTQyODYtOGU3Ny02YTU5OD" \
             "kxNDQzYWMiLCJzZXNzaW9uX3N0YXRlIjoiMTljOTM4MjgtZDFiYy00ZmNkLThiNGQtZTg5ODgzY2VkNDBhIiwiYWNyIjoiMSIsImFs" \
             "bG93ZWQtb3JpZ2lucyI6WyIqIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJBdGxhc19yb2xlX2FkbWluIl19LCJyZXNvdXJjZV9h" \
             "Y2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9ma" \
             "WxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiUGVuZ2ZlaSBM" \
             "aXUiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJwZW5nZmVpIiwiZ2l2ZW5fbmFtZSI6IlBlbmdmZWkiLCJmYW1pbHlfbmFtZSI6IkxpdSIs" \
             "ImVtYWlsIjoibGl1LnBlbmdmZWlAaG90bWFpbC5mciJ9.L_fCJi4i-v4HWTviT2M-qZE7FEIhVdzw886VbdSpOf7eRaTcwCAnOxQ6kx4" \
             "Q7LbCU9GKjw_9auPJLY4WsT2srMz5KgX6WE3WYfko07w01Tf8rh82wMlhhFEo2zW9dbTQv0vVVpLCd_SuZY35QoesmixufFIavkd91m" \
             "Ypri_o1r-Wa3rGsfHtKJNj6znuTzkXPLLFKw3uTGP8FlCoXk0OrIjN6BPryoqSCR05dbKFaKxhaXhdLbzSX5O4gKSdpWgfoYURGzvg89C" \
             "y8j3WORC0qtaRBLIOr1ECS1cDuBvkpa0a5eo5QB2eGpg2t6EIdvDoTN9ntF81mirLbGBBBH2t6g"
atlas_client = Atlas(hostname, port, oidc_token=oidc_token)
s3_bucket_manager = S3BucketManager(atlas_client)

# creat s3 bucket in atlas
s3_bucket_manager.create_entity("test", "s3://test.org", "s3://test.org/test1", "test for me")

# get s3 bucket via guid
# guid = "9642d134-4d0e-467c-8b36-ca73902d4c14"
# e = s3_bucket_manager.get_entity(guid)
# s3_bucket_manager.show_entity_attributes(e)
# e_attributes = s3_bucket_manager.get_entity_attributes(e)
# e_attributes_key_list = s3_bucket_manager.get_s3_attributes_key_list(e)
# print(e_attributes_key_list)
# print(e_attributes['description'])

# update s3 bucket attributes
# s3_bucket_manager.update_entity(guid, 'description', 'update description from api')

# delete s3 bucket
# s3_bucket_manager.delete_entity(guid)

s3_ps_dir_manager = S3PsDirManager(atlas_client)
# s3_ps_dir_manager.create_entity("data_science", "s3://pengfei.org/pengfei_test1/data_science",
#                                 "s3://pengfei.org/pengfei_test1", "data_science/")
#
s3_ps_dir_manager.create_entity("data_science1", "s3://test.org/test1/data_science1",
                               "s3://test.org/test1", "data_science1/")

s3_obj_manager = S3ObjectManager(atlas_client)
s3_obj_manager.create_entity("toto.csv", "s3://test.org/test1/data_science1/toto.csv",
                              "s3://test.org/test1/data_science1", "data_science1/", "csv", "pengfei",
                              "test txt")
