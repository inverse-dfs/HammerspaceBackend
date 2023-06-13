import boto3
from random import randint
from botocore.exceptions import ClientError

BUCKET = 'hammerspace-image-buckettest'
FILE_TYPE = 'pdf'
URL_EXPIRATION_SECONDS = 300

s3 = boto3.client('s3')

def get_upload_url():
    upload_id = randint(0, 10000000)
    key = '.'.join([str(upload_id), FILE_TYPE])

    try:
        signed_url = s3.generate_presigned_post(Bucket=BUCKET, Key=key, Fields=None, Conditions=None, ExpiresIn=URL_EXPIRATION_SECONDS)
        return signed_url
    except ClientError as e:
        print(e)
        return None        
