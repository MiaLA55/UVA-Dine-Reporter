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
        username = request.POST.get('username')
        report_explanation = request.POST.get('reportExplanation')

        # Get the uploaded file
        uploaded_file = request.FILES['file']

        # Create a Report object with the extracted data
        report = Report.objects.create(
            attached_user=username,
            explanation=report_explanation,
            filenames=uploaded_file.name  # Assuming you want to store the filename
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

        context = {
            "reports": reports,
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

        # Initialize an empty list to store file data
        file_data = []

        # Initialize the Amazon S3 client
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        # Define the bucket name
        bucket_name = "dininghallapp"

        # Retrieve all objects from the bucket
        response = s3.list_objects_v2(Bucket=bucket_name)

        # Iterate through objects in the bucket
        for obj in response.get("Contents", []):
            file_name = obj["Key"]

            # Check if the file belongs to the specific user
            if user_identifier in file_name and not file_name.endswith(
                (".txt.txt", ".pdf.txt", ".jpg.txt")
            ):
                # Retrieve report explanation if available
                status = file_name.split("_")[0]
                report_explanation_key = f"{file_name}.txt"
                try:
                    report_obj = s3.get_object(
                        Bucket=bucket_name, Key=report_explanation_key
                    )
                    report_explanation = report_obj["Body"].read().decode("utf-8")
                except s3.exceptions.NoSuchKey:
                    report_explanation = "No report explanation provided"  # Default explanation if not available

                report_resolve_notes_key = f"resolve_notes_for_{file_name}.txt"
                try:
                    report_obj = s3.get_object(
                        Bucket=bucket_name, Key=report_resolve_notes_key
                    )
                    report_resolve_notes = report_obj["Body"].read().decode("utf-8")
                except s3.exceptions.NoSuchKey:
                    report_resolve_notes = "No report resolve notes provided"  # Default explanation if not available

                # Add file_name and report_explanation to the list
                file_data.append(
                    (status, file_name, report_explanation, report_resolve_notes)
                )

        context = {
            "username": request.user.username,
            "file_data": file_data,
            'report_explanation': report_explanation,
            'report_resolve_notes': report_resolve_notes,
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


# def resolve_report_submit(request):
#     if request.user.is_authenticated:
#         user_identifier = request.user

#         if request.method == "POST" and request.FILES.get("file"):
#             current_filename = request.FILES["file"].name
#             s3 = boto3.client(
#                 "s3",
#                 aws_access_key_id=AWS_ACCESS_KEY_ID,
#                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#             )
#             new_filename = f"RESOLVED_{current_filename}"
#             # test downloading
#             s3.download_file(AWS_STORAGE_BUCKET_NAME, current_filename, new_filename)
#             s3.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=current_filename)
#             s3.upload_file(AWS_STORAGE_BUCKET_NAME, new_filename)

#             # delete ./test_passed.txt for future
#             if os.path.isfile(new_filename):
#                 os.remove(new_filename)
#             return redirect("login/list_files.html")

#         else:
#             return HttpResponse("No file selected.")

#     else:
#         return redirect("login")


def resolve_report_submit(request):
    if request.user.is_authenticated:
        user_identifier = request.user

        if request.method == "POST":
            resolve_notes = request.POST.get("resolveNotes", "")
            current_filename = request.POST.get("file_name", "")
            new_filename = f"RESOLVED_{current_filename}"
            s3 = boto3.client(
                "s3",
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            )

            # Copy the file to the new name
            s3.copy_object(
                Bucket=AWS_STORAGE_BUCKET_NAME,
                CopySource={"Bucket": AWS_STORAGE_BUCKET_NAME, "Key": current_filename},
                Key=new_filename,
            )

            # Delete the old file
            s3.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=current_filename)

            if resolve_notes:
                resolve_notes_filename = f"resolve_notes_for_{new_filename}.txt"
                s3.put_object(
                    Body=resolve_notes.encode(),
                    Bucket=AWS_STORAGE_BUCKET_NAME,
                    Key=resolve_notes_filename,
                )
            return render(request, "login/resolve_report.html")

        else:
            return HttpResponse("No file selected.")

    else:
        return redirect("login")


def individual_file_view(request):
    # Retrieve parameters from the URL
    file_name = request.GET.get('file_name')
    status = request.GET.get('status')
    report_explanation = request.GET.get('report_explanation')
    report_resolve_notes = request.GET.get('report_resolve_notes')

    # Check if the status is NEW, then update it to INPROGRESS
    if status.startswith("NEW"):
        # Update the status and file name
        status = "IN PROGRESS"
        new_file_name = f"INPROGRESS_{file_name}"
        s3 = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        # Copy the file to the new name
        s3.copy_object(
            Bucket=AWS_STORAGE_BUCKET_NAME,
            CopySource={"Bucket": AWS_STORAGE_BUCKET_NAME, "Key": file_name},
            Key=new_file_name,
        )

        # Delete the old file
        s3.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=file_name)

        context = {
            'file_name': new_file_name,
            'status': status,
            'report_explanation': report_explanation,
            'report_resolve_notes': report_resolve_notes,
        }
    else:
        context = {
            'file_name': file_name,
            'status': status,
            'report_explanation': report_explanation,
            'report_resolve_notes': report_resolve_notes,
        }


    return render(request, "login/individual_file_view.html", context)