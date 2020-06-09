##########
# Pre-reqs
# * ~/.aws/config
# [default]
# aws_access_key_id = XXX
# aws_secret_access_key = xxxx
# region=ap-southeast-1
import os
from aws_lib import *
import boto3
import logging
from pprint import pformat

if __name__ == "__main__":
    awsLogger = logging.getLogger('awsLogger')
    awsLogger.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    awsLogger.addHandler(streamHandler)

    keyName = 'autogen_key'
    ec2_client = boto3.client('ec2')
    resp = describe_key_pairs(ec2_client=ec2_client)
    awsLogger.debug(pformat(resp))
    resp = delete_key_pair(ec2_client=ec2_client,keyName=keyName)
    awsLogger.debug(pformat(resp))
    resp = create_key_pair(ec2_client=ec2_client,keyName=keyName)
    awsLogger.debug(pformat(resp))
    keyMaterial = resp['KeyMaterial']
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    keyFileName = 'autogen_key.pem'
    with open(keyFileName, 'w') as writer:
        writer.write(keyMaterial)
    os.chmod(keyFileName, 0o600)

    ec2_resource = boto3.resource('ec2')
    resp = create_ec2_instance(
                ec2_resource,
                imageId='ami-09307ddef4fe3b949',
                instanceType='t2.micro',
                keyName=keyName,
                subnetId='subnet-963ce5f1')
    awsLogger.debug(pformat(resp))
