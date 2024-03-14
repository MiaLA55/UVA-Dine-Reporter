from django.conf import settings
from django.test import TestCase
import boto3
from requests import request

class FileUploadTest(TestCase):
    def upload_txt_file(self):
        
        s3 = boto3.client('s3',
                           aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                           aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        s3.upload_fileobj("test.txt", settings.AWS_STORAGE_BUCKET_NAME, "test.txt")

        # test downloading
        s3.download_file(settings.AWS_STORAGE_BUCKET_NAME, "test.txt", "./test.txt")
"""
  def upload_pdf_file(self):
        BUCKET_NAME = 'YOUR-BUCKET-NAME’
        S3_FILE = 'YOUR-MANUALLY-UPLOADED-FILE-NAME'
        LOCAL_NAME = 'YOUR-LOCAL-NAME-FOR-THIS-FILE'

        s3 = boto3.resource('s3')

        # test listing
        bucket = s3.Bucket(BUCKET_NAME)
        for f in bucket.objects.all():
            print(f.key)

        # test downloading
        bucket.download_file(S3_FILE, LOCAL_NAME)

        # test uploading
        data = open('YOUR-LOCAL-FILE', 'rb')
        bucket.put_object(Key='YOUR-FILE-NAME-ON-S3-FOR-THIS-FILE', Body=data)

    def upload_jpg_file(self):
        BUCKET_NAME = 'YOUR-BUCKET-NAME’
        S3_FILE = 'YOUR-MANUALLY-UPLOADED-FILE-NAME'
        LOCAL_NAME = 'YOUR-LOCAL-NAME-FOR-THIS-FILE'

        s3 = boto3.resource('s3')

        # test listing
        bucket = s3.Bucket(BUCKET_NAME)
        for f in bucket.objects.all():
            print(f.key)

        # test downloading
        bucket.download_file(S3_FILE, LOCAL_NAME)

        # test uploading
        data = open('YOUR-LOCAL-FILE', 'rb')
        bucket.put_object(Key='YOUR-FILE-NAME-ON-S3-FOR-THIS-FILE', Body=data)
"""



