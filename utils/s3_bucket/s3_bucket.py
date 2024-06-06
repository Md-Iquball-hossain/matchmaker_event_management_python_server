import boto3
from config import AWS_S3_BUCKET, AWS_S3_ACCESS_KEY, AWS_S3_SECRET_KEY
import os
import uuid

class Uploader:
    def cloudUpload(file, folder):
        s3 = boto3.client(
            's3',
            aws_access_key_id=AWS_S3_ACCESS_KEY,
            aws_secret_access_key=AWS_S3_SECRET_KEY,
            region_name='ap-south-1'
        )
        try:
            ext = os.path.splitext(file.filename)[-1]
            random_filename = str(uuid.uuid4()) + ext
            key = f"match360/{folder}/{random_filename}"
            s3.upload_fileobj(file, AWS_S3_BUCKET, key)
            return True, key
        except Exception as e:
            s3.delete_object(Bucket=AWS_S3_BUCKET, Key="photo")
            return False, str
