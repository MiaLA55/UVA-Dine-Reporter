import boto3
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Create your views here.

def upload_page(request):
    return HttpResponse("Uploading")

def user_submit_report(request):
    return render(request, template_name="file_upload/user_submit_report.html")

def success(request):
    return render(request, template_name="file_upload/success.html")