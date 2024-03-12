from django.test import TestCase
import boto3

class FileUploadTest(TestCase):
    def upload_txt_file(self):
        # constants
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

