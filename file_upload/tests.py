import os

from django.conf import settings
from django.test import TestCase
import boto3


class FileUploadTest(TestCase):
    def test_upload_txt_file(self):
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        s3.upload_file("file_upload/test.txt", settings.AWS_STORAGE_BUCKET_NAME, "test.txt")

        # test downloading
        s3.download_file(settings.AWS_STORAGE_BUCKET_NAME, "test.txt", "test_passed.txt")

        # Assertions for successful download
        self.assertTrue(os.path.isfile("test_passed.txt"), "Downloaded file not found")

        # delete ./test_passed.txt for future
        if os.path.isfile("test_passed.txt"):
            os.remove("test_passed.txt")

    def test_upload_pdf_file(self):
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        s3.upload_file("file_upload/test.pdf", settings.AWS_STORAGE_BUCKET_NAME, "test.pdf")

        # test downloading
        s3.download_file(settings.AWS_STORAGE_BUCKET_NAME, "test.pdf", "test_passed.pdf")

        # Assertions for successful download
        self.assertTrue(os.path.isfile("test_passed.pdf"), "Downloaded file not found")

        # delete ./test_passed.txt for future
        if os.path.isfile("test_passed.pdf"):
            os.remove("test_passed.pdf")

    def test_upload_jpg_file(self):
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        s3.upload_file("file_upload/test.jpg", settings.AWS_STORAGE_BUCKET_NAME, "test.jpg")

        # test downloading
        s3.download_file(settings.AWS_STORAGE_BUCKET_NAME, "test.jpg", "test_passed.jpg")

        # Assertions for successful download
        self.assertTrue(os.path.isfile("test_passed.jpg"), "Downloaded file not found")

        # delete ./test_passed.txt for future
        if os.path.isfile("test_passed.jpg"):
            os.remove("test_passed.jpg")
