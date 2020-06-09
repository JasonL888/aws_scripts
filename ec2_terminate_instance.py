##########
# Pre-reqs
# * ~/.aws/config
# [default]
# aws_access_key_id = XXX
# aws_secret_access_key = xxxx
# region=ap-southeast-1

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

    ec2_client = boto3.client('ec2')
    resp = delete_ec2_instance(
                ec2_client,
                instanceId = 'i-0b3b57681134f9593')
    awsLogger.debug(pformat(resp))

# Sample output
#{'ResponseMetadata': {'HTTPHeaders': {'content-type': 'text/xml;charset=UTF-8',
#                                      'date': 'Tue, 09 Jun 2020 07:18:58 GMT',
#                                      'server': 'AmazonEC2',
#                                      'transfer-encoding': 'chunked',
#                                      'vary': 'accept-encoding',
#                                      'x-amzn-requestid': '7ecd24c4-f21c-4533-b2d0-10fd80bd8851'},
#                      'HTTPStatusCode': 200,
#                      'RequestId': '7ecd24c4-f21c-4533-b2d0-10fd80bd8851',
#                      'RetryAttempts': 0},
# 'TerminatingInstances': [{'CurrentState': {'Code': 32,
#                                            'Name': 'shutting-down'},
#                           'InstanceId': 'i-0bbd374c8de68f58f',
#                           'PreviousState': {'Code': 16, 'Name': 'running'}}]}
