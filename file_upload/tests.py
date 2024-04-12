import os

from django.conf import settings
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
import boto3
from .models import Report
from login.models import User

AWS_ACCESS_KEY_ID = "AKIAU6GD2ERXH4XMKEH5"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "dininghallapp"


class FileUploadTest(TestCase):


    def test_upload_txt_file(self):
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        s3.upload_file("file_upload/test.txt", AWS_STORAGE_BUCKET_NAME, "test.txt")

        # test downloading
        s3.download_file(AWS_STORAGE_BUCKET_NAME, "test.txt", "test_passed.txt")

        # test delete from s3
        s3.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key="test.txt")

        # Assertions for successful download
        self.assertTrue(os.path.isfile("test_passed.txt"), "Downloaded file not found")

        # delete ./test_passed.txt for future
        if os.path.isfile("test_passed.txt"):
            os.remove("test_passed.txt")

    def test_upload_pdf_file(self):
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        s3.upload_file("file_upload/test.pdf", AWS_STORAGE_BUCKET_NAME, "test.pdf")

        # test downloading
        s3.download_file(AWS_STORAGE_BUCKET_NAME, "test.pdf", "test_passed.pdf")

        s3.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key="test.txt")

        # Assertions for successful download
        self.assertTrue(os.path.isfile("test_passed.pdf"), "Downloaded file not found")

        # delete ./test_passed.txt for future
        if os.path.isfile("test_passed.pdf"):
            os.remove("test_passed.pdf")

    def test_upload_jpg_file(self):
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        s3.upload_file("file_upload/test.jpg", AWS_STORAGE_BUCKET_NAME, "test.jpg")

        # test downloading
        s3.download_file(AWS_STORAGE_BUCKET_NAME, "test.jpg", "test_passed.jpg")

        s3.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key="test.txt")

        # Assertions for successful download
        self.assertTrue(os.path.isfile("test_passed.jpg"), "Downloaded file not found")

        # delete ./test_passed.txt for future
        if os.path.isfile("test_passed.jpg"):
            os.remove("test_passed.jpg")

class ReportModelTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username="test_user", password="password")

    def tearDown(self):
        self.test_user.delete()

    def test_report_submission(self):
        report = Report.objects.create(
            attached_user=self.test_user.username,
            explanation="Test explanation",
            filenames="test.txt"
        )

        saved_report = Report.objects.get(pk=report.pk)

        # Check if the report is saved correctly
        self.assertEqual(saved_report.attached_user, self.test_user.username)
        self.assertEqual(saved_report.explanation, "Test explanation")
        self.assertEqual(saved_report.filenames, "test.txt")

        report.delete()
class ReportViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_user = get_user_model().objects.create_user(username="test_user", password="password")
        self.client.force_login(self.test_user)

    def test_no_reports_user_end(self):
        response = self.client.get(reverse("login:user_reports"))
        self.assertContains(response, "No reports submitted by this user.")
        self.assertQuerySetEqual(response.context["file_data"], [])