import boto3
import os

ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

cidr_block = '10.0.0.0/16'
# cidr_block = '172.31.0.0/16'

vpc_response = ec2_client.describe_vpcs(
    Filters=[
        {
            'Name': 'cidr-block-association.cidr-block',
            'Values': [
             cidr_block, #Enter you cidr block here
            ]
        },
    ]
)
ig_response = ec2_client.describe_internet_gateways(
    Filters=[
        {
            'Name': 'cidr-block-association.cidr-block',
            'Values': [
             cidr_block, #Enter you cidr block here
            ]
        },
    ]
)
vpc_resp = response['Vpcs']
if len(response['Vpcs']) > 0:
    for i in resp:
        print(i['VpcId'] + ' is already using that cidr block, pick another one')
        ec2_client.delete_vpc(VpcId=i['VpcId'])

        print(i['VpcId'] + ' she gone')
else:

    print('No vpcs found, DO IT!')

    # create vpc
    vpc = ec2_resource.create_vpc(CidrBlock=cidr_block)
    vpc_name = 'boto_vpc'
    vpc.create_tags(Tags=[{"Key":'Name', "Value":vpc_name}])
    vpc.wait_until_available()

    print('VPC:' + vpc_name + ' ' + vpc.id + ' created!')

    ig = ec2_resource.create_internet_gateway()
    vpc.attach_internet_gateway(InternetGatewayId=ig.id)
    ig.create_tags(Tags=[{"Key":'Name', "Value":vpc_name}])
    print(ig.id)

    # create a route table and a public route
    route_table = vpc.create_route_table()
    route = route_table.create_route(
        DestinationCidrBlock='0.0.0.0/0',
        GatewayId=ig.id
    )
    print(route_table.id)