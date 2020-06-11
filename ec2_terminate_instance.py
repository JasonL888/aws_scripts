import os
from aws_lib import *
import boto3
import botocore
import logging
from pprint import pformat
import importlib
vpc_destroy = importlib.import_module("aws-vpc-destroy.vpc_destroy")

# Setup loggging
awsLogger = logging.getLogger('awsLogger')
awsLogger.setLevel(logging.DEBUG)

def ec2_terminate_instance_logging_setup():
    fileHandler = logging.FileHandler('ec2_terminate_instance.log',mode='w')
    fileHandler.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.INFO)
    awsLogger.addHandler(streamHandler)
    awsLogger.addHandler(fileHandler)

def obtain_input(prompt_str):
    confirm_str = "N"
    while confirm_str.upper() != "Y":
        input_str = input("\n" + prompt_str)
        print("You have entered:[%s]" % input_str)
        confirm_str = input('\nDo you wish to continue (Y/N)? ')
    return(input_str)

def ec2_terminate_instance():
    # Setup current working directory to where this file is
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    ec2_terminate_instance_logging_setup()

    # Setup connectivity to AWS
    ec2_client = boto3.client('ec2')
    ec2_resource = boto3.resource('ec2')

    instanceId = obtain_input("Enter EC2 instance id to terminate:")
    if is_ec2_instance_exist(ec2_resource, instanceId):
        vpcId = get_vpc(ec2_resource,ec2Id=instanceId)
        resp = delete_ec2_instance(ec2_client, instanceId)
        awsLogger.debug(pformat(resp))
        awsLogger.info('EC2 instance %s terminating ... please wait' % instanceId)
        wait_until_ec2_terminated(ec2_client,ec2Id=instanceId)
        awsLogger.info('EC2 instance % terminated')
        sess = boto3.session.Session()
        resp = vpc_destroy.delete_vpc(vpc_id=vpcId, aws_region=sess.region_name)
        awsLogger.debug(pformat(resp))
        awsLogger.info('VPC %s deleted' % vpcId)
    else:
        awsLogger.error("EC2 instance %s does not exist" % instanceId )

if __name__ == "__main__":
    ec2_terminate_instance()
