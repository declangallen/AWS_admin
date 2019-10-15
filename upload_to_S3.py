import boto3
import os
import uuid

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')

# s3_resource.create_bucket(Bucket='dgallens3testpython1',
#                           CreateBucketConfiguration={
#                               'LocationConstraint': 'eu-west-1'})

def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])

def create_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
        'LocationConstraint': current_region})
    print(bucket_name, current_region)
    return bucket_name, bucket_response

# first_bucket_name, first_response = create_bucket(
#     bucket_prefix='dgtest123',
#     s3_connection=s3_resource.meta.client)

first_bucket = s3_resource.Bucket(name='dgallens3testpython')
first_object = s3_resource.Object(
    bucket_name='dgallens3testpython', key='table.txt')

first_object.upload_file('table.txt')

def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
    copy_source = {
        'Bucket': bucket_from_name,
        'Key': file_name
    }
    s3_resource.Object(bucket_to_name, file_name).copy(copy_source)

copy_to_bucket('dgallens3testpython', 'dgallens3testpython1', 'table.txt')