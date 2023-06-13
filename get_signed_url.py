import boto3
import os
import logging
from random import randint
from botocore.exceptions import ClientError

FILE_TYPE = 'pdf'
FILE_CONTENT_TYPE = 'application/pdf'
URL_EXPIRATION_SECONDS = 300
ACL_POLICY = 'public-read'

s3 = boto3.client('s3')

def get_upload_url():
    upload_id = randint(0, 10000000)
    key = '.'.join([str(upload_id), FILE_TYPE])

    bucket = None   
    try:
        bucket = os.environ['UPLOAD_BUCKET']
    except KeyError as e:
        print(e)
        return None

    fields = {
        "ContentType": FILE_CONTENT_TYPE,
        "ACL": ACL_POLICY
    }
    try:
        signed_url = s3.generate_presigned_post(Bucket=bucket, Key=key, Fields=fields, Conditions=None, ExpiresIn=URL_EXPIRATION_SECONDS)
        return signed_url
    except ClientError as e:
        print(e)
        return None        
