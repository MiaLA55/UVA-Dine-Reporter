import os

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from file_upload.models import Report
from django.urls import reverse
import boto3
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone




AWS_ACCESS_KEY_ID = "AKIAU6GD2ERXH4XMKEH5"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "dininghallapp"


def auth_home(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name="Site Admin").exists():
            return render(
                request=request, template_name="login/admin_home.html", context={}
            )
        else:
            return render(
                request=request, template_name="login/auth_home.html", context={}
            )
    elif isinstance(request.user, AnonymousUser):
        return render(request=request, template_name="login/auth_home.html", context={})
    else:
        return render(request, template_name="login/logout.html")


def home(request):
    logout(request)
    return render(request=request, template_name="login/home.html", context={})


def logout_view(request):
    logout(request)
    return render(request, template_name="login/logout.html")


def admin_home(request):
    return render(request, template_name="login/admin_home.html")


class CustomLoginView(LoginView):
    default_template_name = "login/auth_home.html"
    admin_template_name = "login/admin_home.html"  # Template for admin users

    def get_template_names(self):
        # Check if the user belongs to the 'Site Admin' group
        if self.request.user.groups.filter(name="Site Admin").exists():
            return [self.admin_template_name]
        else:
            return [self.default_template_name]

    def get_success_url(self):
        # Redirect users after login
        if self.request.user.groups.filter(name="Site Admin").exists():
            return reverse(
                "admin_dashboard"
            )  # Assuming 'admin_dashboard' is the URL name for admin dashboard
        else:
            return reverse(
                "user_dashboard"
            )  # Assuming 'user_dashboard' is the URL name for user dashboard

    def get(self, request, *args, **kwargs):
        # Ensure proper template rendering
        return render(request, self.get_template_names()[0], self.get_context_data())



def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        username = request.POST.get('username')
        report_explanation = request.POST.get('explanation')

        
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        s3.upload_fileobj(uploaded_file, AWS_STORAGE_BUCKET_NAME, file_name)

        
        report = Report.objects.create(
            attached_user=username,
            explanation=report_explanation,
            filenames=uploaded_file.name,
            submission_time=timezone.now()  
        )
        return render(request, template_name="file_upload/success.html")

    return HttpResponse("No file selected.")



def check_existing_filename(s3_client, bucket_name, file_name):
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    for obj in response.get("Contents", []):
        if obj["Key"] == file_name:
            return True
    return False


def list_files(request):
    if request.user.is_authenticated:
        # Initialize an empty list to store file data
        reports = Report.objects.all()
        # Initialize an empty list to store file data
        file_data = []
        for report in reports:
            file_data.append({
                'status': report.status,
                'file_name': report.filenames,
                'report_explanation': report.explanation,
                'report_resolve_notes': report.resolved_notes,
            })

        context = {
            "username": request.user.username,
            "file_data": file_data,
        }

        return render(request, "login/list_files.html", context)
    else:
        # If the user is not authenticated, redirect them to the login page
        return redirect("login")


def file_detail(request, file_name):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    # Retrieve the file content from S3
    try:
        response = s3.get_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=file_name)
        file_content = response["Body"].read()
    except Exception as e:
        return HttpResponse(f"Error retrieving file: {e}")

    # Determine the content type based on the file extension
    content_type = None
    if file_name.endswith(".txt"):
        content_type = "text/plain"
    elif file_name.endswith(".jpg"):
        content_type = "image/jpeg"
    elif file_name.endswith(".pdf"):
        content_type = "application/pdf"
    else:
        # If the file extension is not recognized, return an error response
        return HttpResponse("Unsupported file type")

    # Return an HTTP response with the file content and appropriate content type
    return HttpResponse(file_content, content_type=content_type)


@login_required
def list_specific_user_files(request):
    if request.user.is_authenticated:
        user_identifier = request.user.username

        reports = Report.objects.filter(attached_user=user_identifier)
        # Initialize an empty list to store file data
        file_data = []
        for report in reports:
            file_data.append({
                'status': report.status,
                'file_name': report.filenames,
                'report_explanation': report.explanation,
                'report_resolve_notes': report.resolved_notes,
            })

        context = {
            "username": request.user.username,
            "file_data": file_data,
        }

        # Render the template with the file data
        return render(request, "login/user_list_files.html", context)
    else:
        # If the user is not authenticated, redirect them to the login page
        return redirect("login")


def resolve_report(request):
    if request.user.is_authenticated:
        user_identifier = request.user.username
        return render(request, "login/resolve_report.html")
    else:
        return redirect("login")


def resolve_report_submit(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            resolve_notes = request.POST.get("resolveNotes", "")
            filename = request.POST.get("file_name", "")

            # Retrieve the specific report based on the file name
            report = get_object_or_404(Report, filenames=filename)

            # Update the resolved_notes field of the report
            report.resolved_notes = resolve_notes
            report.status = 'RESOLVED'
            report.save()

            # Your other code for file handling if needed

            return render(request, "login/resolve_report.html")
        else:
            return HttpResponse("No file selected.")
    else:
        return redirect("login")

def individual_file_view(request):
    # Retrieve the file name from the query parameters
    file_name = request.GET.get('file_name', '')

    # Retrieve the corresponding report from the database
    report = get_object_or_404(Report, filenames=file_name)
    report.status = 'IN PROGRESS'
    report.save()

    # Prepare the context with the details of the specific report
    context = {
        "report": report,
    }

    # Render the individual file view template with the context
    return render(request, "login/individual_file_view.html", context)