import boto3
from random import randint
from botocore.exceptions import ClientError

s3 = boto3.client('s3')

def get_upload_url(bucket: str, file_type: str = 'jpeg', expires_in: int = 300) -> str:
    upload_id = randint(0, 10000000)
    key = '.'.join([str(upload_id), file_type])

    try:
        signed_url = s3.generate_presigned_post(Bucket=bucket, Key=key, Fields=None, Conditions=None, ExpiresIn=expires_in)
        return signed_url
    except ClientError as e:
        print(e)
        return None        
