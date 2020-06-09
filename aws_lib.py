import boto3
import logging
from pprint import pformat

def describe_key_pairs(ec2_client):
    response = ec2_client.describe_key_pairs()
    return(response)
# sample response
#{'KeyPairs': [{'KeyFingerprint': 'cd:1a:d4:8b:de:51:09:c7:7b:10:ef:30:8d:7d:7b:5c:e3:ab:e2:17',
#               'KeyName': 'APAC-Axiros',
#               'KeyPairId': 'key-05c0aa11ae32e6c98',
#               'Tags': []},
#              {'KeyFingerprint': '3d:0c:c9:88:20:ec:d4:51:20:00:42:49:b4:6b:03:93:ad:24:7f:ff',
#               'KeyName': 'yang',
#               'KeyPairId': 'key-09f4b5eb98b96249b',
#               'Tags': []}],
#'ResponseMetadata': {'HTTPHeaders': {'content-length': '2557',
#                                      'content-type': 'text/xml;charset=UTF-8',
#                                      'date': 'Tue, 09 Jun 2020 05:32:03 GMT',
#                                      'server': 'AmazonEC2',
#                                      'vary': 'accept-encoding',
#                                      'x-amzn-requestid': 'b4efb413-5e31-43b3-ac72-56870c6de111'},
#                      'HTTPStatusCode': 200,
#                      'RequestId': 'b4efb413-5e31-43b3-ac72-56870c6de111',
#                      'RetryAttempts': 0}}

def create_key_pair(ec2_client, keyName):
    response = ec2_client.create_key_pair(KeyName=keyName)
    return(response)
# Sample Response
#{'KeyFingerprint': '73:3f:57:a5:47:58:78:58:95:21:cd:46:f4:6e:83:2d:75:3c:d8:c7',
# 'KeyMaterial': '-----BEGIN RSA PRIVATE KEY-----\n'
#                'MIIEpQIBAAKCAQEAv247aj1kPYgOCOwQrW2iw4RoROGhdURfo7qXJG1YtCcZIrVJRqKyNigTlH0E\n'
#                ...
#                'LS6IXQ9LLEfcw0r8GCIGxb61SzjMKlfAKPUNCCcGc9qIA9aB4qE+cMqF9ZgeD6bc0Cgbld0=\n'
#                '-----END RSA PRIVATE KEY-----',
# 'KeyName': 'autogen_key',
# 'KeyPairId': 'key-0b3ecdf231f27c436',
# 'ResponseMetadata': {'HTTPHeaders': {'content-length': '2088',
#                                      'content-type': 'text/xml;charset=UTF-8',
#                                      'date': 'Tue, 09 Jun 2020 05:46:42 GMT',
#                                      'server': 'AmazonEC2',
#                                      'vary': 'accept-encoding',
#                                      'x-amzn-requestid': 'eeca4359-9e6d-45d0-9541-01c3d6c4d0fd'},
#                      'HTTPStatusCode': 200,
#                      'RequestId': 'eeca4359-9e6d-45d0-9541-01c3d6c4d0fd',
#                      'RetryAttempts': 0}}

def delete_key_pair(ec2_client, keyName):
    response = ec2_client.delete_key_pair(KeyName=keyName)
    return(response)
# Surprising no error when keyName does not exist - always get 200 OK

def create_ec2_instance(ec2_resource, imageId,instanceType,keyName,subnetId):
    instances = ec2_resource.create_instances(
        ImageId=imageId,
        MinCount=1,
        MaxCount=1,
        InstanceType=instanceType,
        KeyName=keyName,
        SubnetId=subnetId
    )
    return(instances)

def delete_ec2_instance(ec2_client, instanceId):
    response = ec2_client.terminate_instances(InstanceIds=[instanceId])
    return(response)


