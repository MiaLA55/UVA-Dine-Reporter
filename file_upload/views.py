from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def upload_page(request):
    return HttpResponse("Uploading")

def user_submit_report(request):
    return render(request, template_name="file_upload/user_submit_report.html")