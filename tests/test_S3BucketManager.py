import json

from atlaspyapi.entity_source_generation.S3BucketEntityGenerator import S3BucketEntityGenerator


def test_generate_s3_bucket_json_source():
    generated_json_str = S3BucketEntityGenerator.generate_s3_bucket_json_source("pengfei", "minio.lab.sspcloud.fr",
                                                                                "for test")
    expected_result = {
        "entity": {
            "status": "ACTIVE",
            "createdBy": "admin",
            "updatedBy": "admin",
            "version": 0,
            "typeName": "aws_s3_bucket",
            "attributes": {
                "owner": "null",
                "qualifiedName": "s3a://minio.lab.sspcloud.fr/pengfei",
                "encryptionType": "none",
                "description": "for test",
                "partner": "none",
                "domain": "minio.lab.sspcloud.fr",
                "isEncrypted": False,
                "name": "pengfei",
                "region": "none"
            }
        }
    }
    generated_result = json.loads(generated_json_str)
    del generated_result["entity"]["createTime"]
    del generated_result["entity"]["updateTime"]
    del generated_result["entity"]["attributes"]["createtime"]
    assert generated_result == expected_result
