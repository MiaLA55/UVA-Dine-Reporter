import boto3
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

# Create your views here.

def upload_page(request):
    return HttpResponse("Uploading")

def user_submit_report(request):
    if request.method == 'POST':
        # Extract report explanation
        report_explanation = request.POST.get('reportExplanation', '')

        # Extract uploaded file
        uploaded_file = request.FILES.get('file')

        # Save uploaded file to S3
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        s3.upload_fileobj(uploaded_file, settings.AWS_STORAGE_BUCKET_NAME, uploaded_file.name)

        # Save report explanation and S3 file link as one report
        report_data = f"Report Explanation: {report_explanation}\nS3 File Link: {uploaded_file.name}"

        # Save report data to S3 or any other desired storage mechanism
        file_name = 'report.txt'  # Choose a suitable file name
        default_storage.save(file_name, ContentFile(report_data))
        return render(request, template_name="file_upload/user_submit_report.html")

    return render(request, template_name="file_upload/user_submit_report.html")

def success(request):
    return render(request, template_name="file_upload/success.html")