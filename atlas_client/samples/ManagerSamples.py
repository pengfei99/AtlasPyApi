from atlas_client.client import Atlas
from atlas_client.entity_management.s3.S3BucketManager import S3BucketManager

hostname = "https://atlas.lab.sspcloud.fr"
port = 443
oidc_token="eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJhUHNCSzhYRC1od1gtMWJFbjdZZDRLS0tWS0hYRy03RHg3STZDaVZZWUtRIn0.eyJleHAiOjE2MDMyMjE3MTcsImlhdCI6MTYwMzE4MjI4NywiYXV0aF90aW1lIjoxNjAzMTc4NTE3LCJqdGkiOiJhYWY2NDNjZC0wZmU1LTQ5ZWUtYjlhYi0wMzZmZjUyMWNjZWEiLCJpc3MiOiJodHRwczovL2F1dGgubGFiLnNzcGNsb3VkLmZyL2F1dGgvcmVhbG1zL3NzcGNsb3VkIiwiYXVkIjpbIm9ueXhpYSIsImFjY291bnQiXSwic3ViIjoiNDczNDkxMjgtNGE0Yy00MjI2LWE1YjEtNjgwODAxYWY1YTJiIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoib255eGlhIiwibm9uY2UiOiI2YmU3NmIwMy05NGIwLTQwZjYtODNlNS0wNjU5NWY5OWE2MjciLCJzZXNzaW9uX3N0YXRlIjoiNjdiM2Q4OGUtOThiZS00MmQwLTkxYmMtMDkzZDFlMmEwNTkyIiwiYWNyIjoiMCIsImFsbG93ZWQtb3JpZ2lucyI6WyIqIl0sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJBdGxhc19yb2xlX2FkbWluIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiUGVuZ2ZlaSBMaXUiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJwZW5nZmVpIiwiZ2l2ZW5fbmFtZSI6IlBlbmdmZWkiLCJmYW1pbHlfbmFtZSI6IkxpdSIsImVtYWlsIjoibGl1LnBlbmdmZWlAaG90bWFpbC5mciJ9.lLNeJ8vyi8AD6evIS2UnbH2UdkVmI7rVtX5Ah-38_iNL2-pQ6-AeynU8jrHlxxpV_I0SEAC8GkADkuGlQFMfR5g8NMFIC9GSD3rbDfspPxM7f-GBUHY0dMgeqJxtRTNePVnEsPox4bP5xttIIAjCrfEjwDHUbCuldcm82HAsbDJwGu5GCbQKf6CNiyZEXWw-u-ncZbHUxO3eiZ4H0RNHy93WXWEpPZ6Il96f-Pn4Muef5yPraoDliarCoSQPylTK61lKrQyzdOLUxb23lfJEgQzb6bUJXtUiu8mQZpM4Jipl2PUgIKqJ7rAuRgACvMRDskQgXUewA3PUkh-YpW2Cyg"

atlas_client = Atlas(hostname, port, oidc_token=oidc_token)
s3_bucket_manager = S3BucketManager(atlas_client)

# creat s3 bucket in atlas
s3_bucket_manager.create_entity("test", "s3://test.org", "s3://test.org/test", "test for me")

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

# s3_ps_dir_manager = S3PsDirManager(hostname, port, login, pwd)
# s3_ps_dir_manager.create_entity("data_science", "s3://pengfei.org/pengfei_test1/data_science",
#                                 "s3://pengfei.org/pengfei_test1", "data_science/")
#
# s3_ps_dir_manager.create_entity("data_science1", "s3://pengfei.org/pengfei_test1/data_science1",
#                                 "s3://pengfei.org/pengfei_test1", "data_science1/")

# s3_obj_manager = S3ObjectManager(atlas_client)
# s3_obj_manager.create_entity("toto.csv", "s3://pengfei.org/pengfei_test1/data_science/toto.csv",
#                              "s3://pengfei.org/pengfei_test1/data_science", "data_science", "csv", "pengfei",
#                              "test txt")
