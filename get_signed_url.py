import boto3
from random import randint
from botocore.exceptions import ClientError

BUCKET = 'hammerspace-image-buckettest'
URL_EXPIRATION_SECONDS = 300

s3 = boto3.client('s3')

def get_upload_url(file_type: str):
    upload_id = randint(0, 10000000)
    key = '.'.join([str(upload_id), file_type])

    try:
        signed_url = s3.generate_presigned_post(Bucket=BUCKET, Key=key, Fields=None, Conditions=None, ExpiresIn=URL_EXPIRATION_SECONDS)
        print("got signed url", signed_url)
        return signed_url
    except ClientError as e:
        print(e)
        return None        
