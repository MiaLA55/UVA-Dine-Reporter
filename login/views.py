from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
import boto3
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser


# views.py

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
        file = request.FILES["file"]
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        s3.upload_fileobj(file, AWS_STORAGE_BUCKET_NAME, file.name)
        return HttpResponse("File uploaded successfully.")
    return HttpResponse("No file selected.")


def list_files(request):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    bucket_name = "dininghallapp"
    response = s3.list_objects_v2(Bucket=bucket_name)

    file_names = [obj["Key"] for obj in response["Contents"]]
    return render(request, "login/list_files.html", {"file_names": file_names})


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
