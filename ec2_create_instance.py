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

# Setup loggging
awsLogger = logging.getLogger('awsLogger')
awsLogger.setLevel(logging.DEBUG)

def ec2_create_instance_logging_setup():
    fileHandler = logging.FileHandler('ec2_create_instance.log',mode='w')
    fileHandler.setLevel(logging.DEBUG)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.INFO)
    awsLogger.addHandler(streamHandler)
    awsLogger.addHandler(fileHandler)

def ec2_create_instance():
    # Setup current working directory to where this file is
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    ec2_create_instance_logging_setup()

    # Setup connectivity to AWS
    ec2_client = boto3.client('ec2')
    ec2_resource = boto3.resource('ec2')

    # Reuse if not setup new key pair
    keyName = 'ec2_create_instance'
    keyFileName = '%s.pem' % keyName
    if ( not os.path.isfile(keyFileName) ):
        resp = describe_key_pairs(ec2_client=ec2_client)
        awsLogger.debug(pformat(resp))
        resp = delete_key_pair(ec2_client=ec2_client,keyName=keyName)
        awsLogger.debug(pformat(resp))
        resp = create_key_pair(ec2_client=ec2_client,keyName=keyName)
        awsLogger.debug(pformat(resp))
        keyMaterial = resp['KeyMaterial']
        with open(keyFileName, 'w') as writer:
            writer.write(keyMaterial)
        os.chmod(keyFileName, 0o600)
        awsLogger.info('key file %s generated' % keyFileName)
    else:
        awsLogger.info('key file %s exist, will reuse' % keyFileName)

    # Setup VPC - which auto creates a route table
    vpc_resp = create_VPC(ec2_client)
    awsLogger.debug(pformat(vpc_resp))
    vpcId = vpc_resp['Vpc']['VpcId']
    awsLogger.info('VPC %s created' % vpcId)

    # Setup InternetGateway and associate with VPC
    gwResp = create_internet_gateway(ec2_resource)
    awsLogger.debug(pformat(gwResp))
    gwId = gwResp.id
    awsLogger.info('Internet Gateway %s created' % gwId)

    attachGwResp = attach_internet_gateway(ec2_client,internetGatewayId=gwId,vpcId=vpcId)
    awsLogger.debug(pformat(attachGwResp))
    awsLogger.info('Internet Gateway %s attached to VPC %s' % (gwId,vpcId))

    # Setup RouteTable and Route to InternetGateway
    #routeTableResp = create_route_table(ec2_client,vpcId=vpcId)
    #awsLogger.debug(pformat(routeTableResp))
    #routeTableId = routeTableResp['RouteTable']['RouteTableId']
    #awsLogger.info('Route Table %s created', routeTableId)

    # Obtain routeTableId from VPC created
    routeTableId = get_route_table_from_vpc(ec2_resource, vpcId=vpcId)
    awsLogger.info('Route Table %s from Vpc %s' % (vpcId, routeTableId))

    routeResp = create_route(ec2_client, destinationCidrBlock='0.0.0.0/0', gatewayId=gwId, routeTableId=routeTableId)
    awsLogger.debug(pformat(routeResp))
    awsLogger.info('Default Route to Gateway %s created and attached to RouteTable %s' % (gwId, routeTableId))

    # Setup SecurityGroup and ingress rules
    secGroupResp = create_security_group(ec2_client,vpcId=vpcId)
    awsLogger.debug(pformat(secGroupResp))
    secGroupId = secGroupResp['GroupId']
    awsLogger.info('Security Group %s created' % secGroupId)

    secGroupIngressResp = authorize_security_group_ingress(ec2_client,groupId=secGroupId)
    awsLogger.debug(pformat(secGroupIngressResp))
    awsLogger.info('Security Group Ingress created')


    # Setup Subnet and associate with VPC
    subnetResp = create_subnet(ec2_client,vpcId=vpcId)
    subnetId = subnetResp['Subnet']['SubnetId']
    awsLogger.debug(pformat(subnetResp))
    awsLogger.info('Subnet %s created' % subnetId)

    ec2CreateResp = create_ec2_instance(
                ec2_resource,
                imageId='ami-09307ddef4fe3b949',
                instanceType='t2.micro',
                keyName=keyName,
                subnetId=subnetId,
                securityGroupId=secGroupId,
                )
    awsLogger.debug(pformat(ec2CreateResp))
    ec2Id = ec2CreateResp[0].id
    awsLogger.info('EC2 instance %s created', ec2Id)


if __name__ == "__main__":
    ec2_create_instance()
