import boto3
from botocore.exceptions import ClientError
import os

class FileServer:
    def __init__(self):
        pass
    
    def Upload(self, file_name, filetype, bucket="hammerspace-download-bucket"):
        """Upload a file to an S3 bucket

        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        object_name = os.path.basename(file_name)

        # Upload the file
        s3_client = boto3.client('s3')
        extra_args = {
            'ContentType': 'application/pdf'
        }
        try:
            response = s3_client.upload_file(file_name, bucket, object_name, ExtraArgs=extra_args)
        except ClientError as e:
            print(e)
            return ''
        return object_name

    def Download(self, fileid, bucket='hammerspace-image-buckettest'):
        s3 = boto3.client('s3')
        s3.download_file(Bucket=bucket, Key=fileid, Filename=fileid)