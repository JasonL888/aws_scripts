import boto3
import logging
from pprint import pformat


# Key Pairs
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

# Subnet for VPC
def create_subnet(ec2_client, vpcId):
    response = ec2_client.create_subnet(CidrBlock='172.30.1.0/24', VpcId=vpcId)
    return(response)
# Sample response
#{'ResponseMetadata': {'HTTPHeaders': {'content-length': '939',
#                                      'content-type': 'text/xml;charset=UTF-8',
#                                      'date': 'Tue, 09 Jun 2020 09:27:10 GMT',
#                                      'server': 'AmazonEC2',
#                                      'x-amzn-requestid': 'c0e70824-1e25-4309-bd42-98294c5dafbc'},
#                      'HTTPStatusCode': 200,
#                      'RequestId': 'c0e70824-1e25-4309-bd42-98294c5dafbc',
#                      'RetryAttempts': 0},
# 'Subnet': {'AssignIpv6AddressOnCreation': False,
#            'AvailabilityZone': 'ap-southeast-1c',
#            'AvailabilityZoneId': 'apse1-az3',
#            'AvailableIpAddressCount': 251,
#            'CidrBlock': '172.30.1.0/24',
#            'DefaultForAz': False,
#            'Ipv6CidrBlockAssociationSet': [],
#            'MapPublicIpOnLaunch': False,
#            'OwnerId': '214228110897',
#            'State': 'pending',
#            'SubnetArn': 'arn:aws:ec2:ap-southeast-1:214228110897:subnet/subnet-0092ead57d6ad3631',
#            'SubnetId': 'subnet-0092ead57d6ad3631',
#            'VpcId': 'vpc-0ae5f0f3f93dcaf18'}}

# VPC
def create_VPC(ec2_client):
    response = ec2_client.create_vpc(
        CidrBlock='172.30.0.0/16',
        AmazonProvidedIpv6CidrBlock=True,
        InstanceTenancy='default'
        )
    return(response)
# sample Response
#'Vpc': {'CidrBlock': '172.30.0.0/16',
#         'CidrBlockAssociationSet': [{'AssociationId': 'vpc-cidr-assoc-025a3be63bee3a468',
#                                      'CidrBlock': '172.30.0.0/16',
#                                      'CidrBlockState': {'State': 'associated'}}],
#         'DhcpOptionsId': 'dopt-964776f2',
#         'InstanceTenancy': 'default',
#         'Ipv6CidrBlockAssociationSet': [{'AssociationId': 'vpc-cidr-assoc-006b79f0f4fca14ad',
#                                          'Ipv6CidrBlock': '',
#                                          'Ipv6CidrBlockState': {'State': 'associating'},
#                                          'Ipv6Pool': 'Amazon',
#                                          'NetworkBorderGroup': 'ap-southeast-1'}],
#         'IsDefault': False,
#         'OwnerId': '214228110897',
#         'State': 'pending',
#         'VpcId': 'vpc-0ae5f0f3f93dcaf18'}}
#Note: Deleting this VPC will also delete these objects associated with this VPC in this region:
#Subnets
#Security Groups
#Network ACLs
#Internet Gateways
#Egress Only Internet Gateways
#Route Tables
#Network Interfaces
#Peering Connections
#Endpoints

# Internet Gateway
def create_internet_gateway(ec2_resource):
    response = ec2_resource.create_internet_gateway()
    return(response)
# sample Response
#ec2.InternetGateway(id='igw-0e402526a44cd2093')

def attach_internet_gateway(ec2_client,internetGatewayId,vpcId):
    response = ec2_client.attach_internet_gateway(InternetGatewayId=internetGatewayId,VpcId=vpcId)
    return(response)
# 200 OK

# Route table
def get_route_table_from_vpc(ec2_resource, vpcId):
    vpc = ec2_resource.Vpc(vpcId)
    routeTableList = list(vpc.route_tables.all())
    return( routeTableList[0].id )

def create_route_table(ec2_client,vpcId):
    response = ec2_client.create_route_table(VpcId=vpcId)
    return(response)
# sample
#{'ResponseMetadata': {'HTTPHeaders': {'content-length': '1010',
#                                      'content-type': 'text/xml;charset=UTF-8',
#                                      'date': 'Wed, 10 Jun 2020 08:33:14 GMT',
#                                      'server': 'AmazonEC2',
#                                      'x-amzn-requestid': 'f7077840-4dcb-4b37-9393-6d237c118989'},
#                      'HTTPStatusCode': 200,
#                      'RequestId': 'f7077840-4dcb-4b37-9393-6d237c118989',
#                      'RetryAttempts': 0},
# 'RouteTable': {'Associations': [],
#                'OwnerId': '214228110897',
#                'PropagatingVgws': [],
#                'RouteTableId': 'rtb-01db2c073aa3cfaef',
#                'Routes': [{'DestinationCidrBlock': '172.30.0.0/16',
#                            'GatewayId': 'local',
#                            'Origin': 'CreateRouteTable',
#                            'State': 'active'},
#                           {'DestinationIpv6CidrBlock': '2406:da18:15b:fc00::/56',
#                            'GatewayId': 'local',
#                            'Origin': 'CreateRouteTable',
#                            'State': 'active'}],
#                'Tags': [],
#                'VpcId': 'vpc-0ae5f0f3f93dcaf18'}}

def create_route(ec2_client,destinationCidrBlock,gatewayId,routeTableId):
    response = ec2_client.create_route(
        DestinationCidrBlock=destinationCidrBlock,
        GatewayId=gatewayId,
        RouteTableId=routeTableId,
    )
# resp None


# Security Groups
def create_security_group(ec2_client,vpcId):
    response = ec2_client.create_security_group(
        Description='Sec Group For %s' % vpcId,
        GroupName='Sec Group For %s' % vpcId,
        VpcId=vpcId
    )
    return(response)
# sample Response
#{'GroupId': 'sg-08d39c6841ba4ed7a',
# 'ResponseMetadata': {'HTTPHeaders': {'content-length': '283',
#                                      'content-type': 'text/xml;charset=UTF-8',
#                                      'date': 'Tue, 09 Jun 2020 09:07:25 GMT',
#                                      'server': 'AmazonEC2',
#                                      'x-amzn-requestid': 'bc288548-c1df-4aea-8759-b8252dbf37d4'},
#                      'HTTPStatusCode': 200,
#                      'RequestId': 'bc288548-c1df-4aea-8759-b8252dbf37d4',
#                      'RetryAttempts': 0}}

def authorize_security_group_ingress(ec2_client, groupId):
    response = ec2_client.authorize_security_group_ingress(
        GroupId=groupId,
        IpPermissions=[
            {
                'FromPort': 22,
                'IpProtocol': 'tcp',
                'IpRanges': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'SSH access from anywhere'
                    }
                ],
                'ToPort': 22,
            }

        ]
    )


# EC2
def create_ec2_instance(ec2_resource, imageId,instanceType,keyName,subnetId,securityGroupId):
    instances = ec2_resource.create_instances(
        ImageId=imageId,
        MinCount=1,
        MaxCount=1,
        InstanceType=instanceType,
        KeyName=keyName,
        NetworkInterfaces=[
            {
                'SubnetId':subnetId,
                'DeviceIndex': 0,
                'AssociatePublicIpAddress': True,
                'Groups': [securityGroupId],
            }
        ],
    )
    return(instances)
# [ec2.Instance(id='i-07bcbcf33fc89c374')]

def wait_until_ec2_running(ec2_client, ec2Id):
    waiter = ec2_client.get_waiter('instance_running')
    waiter.wait(
        InstanceIds=[ec2Id],
        WaiterConfig={
            'Delay': 5,
            'MaxAttempts': 24,
        }
    )

def wait_until_ec2_terminated(ec2_client,ec2Id):
    waiter = ec2_client.get_waiter('instance_terminated')
    waiter.wait(
        InstanceIds=[ec2Id],
        WaiterConfig={
            'Delay': 5,
            'MaxAttempts': 24,
        }
    )

def get_ec2_public_ip_address(ec2_resource,ec2Id):
    instance = ec2_resource.Instance(ec2Id)
    return(instance.public_ip_address)

def get_vpc(ec2_resource,ec2Id):
    instance = ec2_resource.Instance(ec2Id)
    return(instance.vpc_id)

def is_ec2_instance_exist(ec2_resource,ec2Id):
    try:
        instance = get_vpc(ec2_resource,ec2Id)
        return(True)
    except:
        return(False)

def delete_ec2_instance(ec2_client, instanceId):
    response = ec2_client.terminate_instances(InstanceIds=[instanceId])
    return(response)
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
