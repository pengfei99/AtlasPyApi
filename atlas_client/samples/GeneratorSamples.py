from atlas_client.entity_source_generation.S3BucketEntityGenerator import S3BucketEntityGenerator
from atlas_client.entity_source_generation.S3PsDirEntityGenerator import S3PsDirEntityGenerator
from atlas_client.entity_source_generation.S3ObjectEntityGenerator import S3ObjectEntityGenerator

# generate a aws_s3_bucket entity json source file
s3_bucket_json_source = S3BucketEntityGenerator.generate_s3_bucket_json_source("donnees-insee", "minio.lab.sspcloud.fr",
                                                                               "s3://minio.lab.sspcloud.fr/donnees-insee",
                                                                               " open data"
                                                                               , creator_id="pliu")
print(s3_bucket_json_source)

# generate a aws_ps_dir
s3_ps_dir_json_source = S3PsDirEntityGenerator.generate_s3_ps_dir_entity_json_source("pengfei",
                                                                                     "s3://minio.lab.sspcloud.fr/donnees-insee/pengfei",
                                                                                     "s3://minio.lab.sspcloud.fr/donnees-insee",
                                                                                     "pengfei/")
print(s3_ps_dir_json_source)

s3_object_json_source = S3ObjectEntityGenerator.generate_s3_object_entity_json_source("toto2.txt",
                                                                                      "s3://minio.lab.sspcloud.fr/donnees-insee/RP/toto2.txt",
                                                                                      "s3://minio.lab.sspcloud.fr/donnees-insee/RP",
                                                                                      "RP/",
                                                                                      "txt", "pliu", "my test8 doc",
                                                                                      size=12048)
print(s3_object_json_source)
