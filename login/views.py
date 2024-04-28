import os
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from file_upload.models import Report, Tag
from django.urls import reverse
import boto3
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

AWS_ACCESS_KEY_ID = "AKIAU6GD2ERXH4XMKEH5"
AWS_SECRET_ACCESS_KEY = "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"
AWS_STORAGE_BUCKET_NAME = "dininghallapp"


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page or perform any other actions
            return redirect('success_url')
        else:
            # If authentication fails, display an error message
            messages.error(request, 'Invalid username or password.')
    # If the request method is GET or authentication fails, render the login form
    return render(request, 'login/home.html')


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
    if request.method == "POST":
        if not request.FILES.get("file") and not request.POST.get("explanation"):
            error_message = "Please provide either a file or an explanation."
            available_tags = Tag.objects.all()
            return render(
                request,
                "file_upload/user_submit_report.html",
                {"error_message": error_message, "available_tags": available_tags},
            )

        if request.FILES.get("file"):
            s3 = boto3.client(
                "s3",
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            )
            uploaded_file = request.FILES["file"]
            file_name = uploaded_file.name
            accepted_extensions = ["txt", "pdf", "jpg"]
            file_extension = file_name.split(".")[-1]
            if file_extension not in accepted_extensions:
                error_message = f"Unsupported file type: {file_extension}"
                available_tags = Tag.objects.all()
                return render(
                    request,
                    "file_upload/user_submit_report.html",
                    {"error_message": error_message, "available_tags": available_tags},
                )

            s3.upload_fileobj(uploaded_file, AWS_STORAGE_BUCKET_NAME, file_name)

            username = request.POST.get("username")
            report_explanation = request.POST.get("explanation")
            location = request.POST.get("location")
            rating = request.POST.get("rating")

            # Get the comma-separated string of tag IDs
            selected_tags_str = request.POST.get("tags", "")

            # Convert the comma-separated string to a list of integers
            selected_tags_ids = [int(tag_id) for tag_id in selected_tags_str.split(",") if tag_id.isdigit()]

            # Create the report object
            report = Report.objects.create(
                attached_user=username,
                explanation=report_explanation,
                filenames=file_name,
                location=location,
                rating=rating,
            )

            # Add the selected tags to the report
            report.tags.add(*selected_tags_ids)

            return render(request, template_name="file_upload/success.html")
        elif request.POST.get("explanation"):
            username = request.POST.get("username")
            report_explanation = request.POST.get("explanation")
            location = request.POST.get("location")
            rating = request.POST.get("rating")

            # Get the comma-separated string of tag IDs
            selected_tags_str = request.POST.get("tags", "")

            # Convert the comma-separated string to a list of integers
            selected_tags_ids = [int(tag_id) for tag_id in selected_tags_str.split(",") if tag_id.isdigit()]

            # Create the report object
            report = Report.objects.create(
                attached_user=username,
                explanation=report_explanation,
                location=location,
                rating=rating,
            )
            report.tags.add(*selected_tags_ids)
            return render(request, template_name="file_upload/success.html")

    return HttpResponse("Nothing uploaded.")


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
            file_data.append(
                {
                    "status": report.status,
                    "file_name": report.filenames,
                    "report_explanation": report.explanation,
                    "submission_time": report.submission_time,
                    "report_resolve_notes": report.resolved_notes,
                    "id": report.id,
                    "location": report.location,
                    "rating": report.rating
                }
            )

        context = {
            "username": request.user.username,
            "file_data": file_data,
        }

        return render(request, "login/list_files.html", context)
    else:
        # If the user is not authenticated, redirect them to the login page
        return redirect("login")


def list_files_new(request):
    if request.user.is_authenticated:
        # Initialize an empty list to store file data
        reports = Report.objects.filter(status="NEW")
        # Initialize an empty list to store file data
        file_data = []
        for report in reports:
            file_data.append(
                {
                    "status": report.status,
                    "file_name": report.filenames,
                    "report_explanation": report.explanation,
                    "submission_time": report.submission_time,
                    "report_resolve_notes": report.resolved_notes,
                    "id": report.id,
                    "location": report.location,
                    "rating": report.rating
                }
            )

        context = {
            "username": request.user.username,
            "file_data": file_data,
        }

        return render(request, "login/list_files_new.html", context)
    else:
        # If the user is not authenticated, redirect them to the login page
        return redirect("login")


def list_files_ip(request):
    if request.user.is_authenticated:
        # Initialize an empty list to store file data
        reports = Report.objects.filter(status="IN PROGRESS")
        # Initialize an empty list to store file data
        file_data = []
        for report in reports:
            file_data.append(
                {
                    "status": report.status,
                    "file_name": report.filenames,
                    "report_explanation": report.explanation,
                    "submission_time": report.submission_time,
                    "report_resolve_notes": report.resolved_notes,
                    "id": report.id,
                    "location": report.location,
                    "rating": report.rating
                }
            )

        context = {
            "username": request.user.username,
            "file_data": file_data,
        }

        return render(request, "login/list_files_ip.html", context)
    else:
        # If the user is not authenticated, redirect them to the login page
        return redirect("login")


def list_files_resolved(request):
    if request.user.is_authenticated:
        # Initialize an empty list to store file data
        reports = Report.objects.filter(status="RESOLVED")
        # Initialize an empty list to store file data
        file_data = []
        for report in reports:
            file_data.append(
                {
                    "status": report.status,
                    "file_name": report.filenames,
                    "report_explanation": report.explanation,
                    "submission_time": report.submission_time,
                    "report_resolve_notes": report.resolved_notes,
                    "id": report.id,
                    "location": report.location,
                    "rating": report.rating,
                    "attached_user": report.attached_user,
                }
            )

        context = {
            "username": request.user.username,
            "file_data": file_data,
        }

        return render(request, "login/list_files_resolved.html", context)
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
            file_data.append(
                {
                    "status": report.status,
                    "file_name": report.filenames,
                    "report_explanation": report.explanation,
                    "report_resolve_notes": report.resolved_notes,
                    "submission_time": report.submission_time,
                    "id": report.id,
                    "tags": report.tags.all(),
                    "location": report.location,
                    "rating": report.rating,
                }
            )

        context = {
            "username": request.user.username,
            "file_data": file_data,
        }

        # Render the template with the file data
        return render(request, "login/user_list_files.html", context)
    else:
        # If the user is not authenticated, redirect them to the login page
        return redirect("login")


@login_required
def user_list_files_new(request):
    if request.user.is_authenticated:
        user_identifier = request.user.username

        reports = Report.objects.filter(attached_user=user_identifier, status="NEW")
        # Initialize an empty list to store file data
        file_data = []
        for report in reports:
            file_data.append(
                {
                    "status": report.status,
                    "file_name": report.filenames,
                    "report_explanation": report.explanation,
                    "report_resolve_notes": report.resolved_notes,
                    "submission_time": report.submission_time,
                    "id": report.id,
                    "tags": report.tags.all(),
                    "location": report.location,
                    "rating": report.rating,
                }
            )

        context = {
            "username": request.user.username,
            "file_data": file_data,
        }

        # Render the template with the file data
        return render(request, "login/user_list_files_new.html", context)
    else:
        # If the user is not authenticated, redirect them to the login page
        return redirect("login")


@login_required
def user_list_files_ip(request):
    if request.user.is_authenticated:
        user_identifier = request.user.username

        reports = Report.objects.filter(
            attached_user=user_identifier, status="IN PROGRESS"
        )
        # Initialize an empty list to store file data
        file_data = []
        for report in reports:
            file_data.append(
                {
                    "status": report.status,
                    "file_name": report.filenames,
                    "report_explanation": report.explanation,
                    "report_resolve_notes": report.resolved_notes,
                    "submission_time": report.submission_time,
                    "id": report.id,
                    "tags": report.tags.all(),
                    "location": report.location,
                    "rating": report.rating,
                }
            )

        context = {
            "username": request.user.username,
            "file_data": file_data,
        }

        # Render the template with the file data
        return render(request, "login/user_list_files_ip.html", context)
    else:
        # If the user is not authenticated, redirect them to the login page
        return redirect("login")


@login_required
def user_list_files_resolved(request):
    if request.user.is_authenticated:
        user_identifier = request.user.username

        reports = Report.objects.filter(
            attached_user=user_identifier, status="RESOLVED"
        )
        # Initialize an empty list to store file data
        file_data = []
        for report in reports:
            file_data.append(
                {
                    "status": report.status,
                    "file_name": report.filenames,
                    "report_explanation": report.explanation,
                    "report_resolve_notes": report.resolved_notes,
                    "submission_time": report.submission_time,
                    "id": report.id,
                    "tags": report.tags.all(),
                    "location": report.location,
                    "rating": report.rating,
                }
            )

        context = {
            "username": request.user.username,
            "file_data": file_data,
        }

        # Render the template with the file data
        return render(request, "login/user_list_files_resolved.html", context)
    else:
        # If the user is not authenticated, redirect them to the login page
        return redirect("login")


def resolve_report(request):
    if request.user.is_authenticated:
        user_identifier = request.user.username
        return render(request, "login/resolve_report.html")
    else:
        return redirect("login")


def resolve_report_submit(request, report_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            resolve_notes = request.POST.get("resolveNotes", "")
            filename = request.POST.get("file_name", "")

            # Retrieve the specific report based on the file name
            report = get_object_or_404(Report, pk=report_id)

            # Update the resolved_notes field of the report
            report.resolved_notes = resolve_notes
            report.status = "RESOLVED"
            report.save()

            # Your other code for file handling if needed

            return render(request, "login/resolve_report.html")
        else:
            return HttpResponse("No file selected.")
    else:
        return redirect("login")


def user_file_view(request, report_id):
    # Retrieve the corresponding report from the database
    prevPage = request.GET.get('prevPage')
    report = get_object_or_404(Report, pk=report_id)

    # Prepare the context with the details of the specific report
    context = {
        "report": report,
        "prevPage": prevPage
    }

    # Render the individual file view template with the context
    return render(request, "login/user_file_view.html", context)


def individual_file_view(request, report_id):
    # Retrieve the corresponding report from the database
    report = get_object_or_404(Report, pk=report_id)
    if report.status != "RESOLVED":
        report.status = "IN PROGRESS"
        report.save()

    # Prepare the context with the details of the specific report
    context = {
        "report": report,
    }

    # Render the individual file view template with the context
    return render(request, "login/individual_file_view.html", context)


def individual_file_view_new(request, report_id):
    # Retrieve the corresponding report from the database
    report = get_object_or_404(Report, pk=report_id)
    if report.status != "RESOLVED":
        report.status = "IN PROGRESS"
        report.save()

    # Prepare the context with the details of the specific report
    context = {
        "report": report,
    }

    # Render the individual file view template with the context
    return render(request, "login/individual_file_view_new.html", context)


def individual_file_view_ip(request, report_id):
    # Retrieve the corresponding report from the database
    report = get_object_or_404(Report, pk=report_id)
    if report.status != "RESOLVED":
        report.status = "IN PROGRESS"
        report.save()

    # Prepare the context with the details of the specific report
    context = {
        "report": report,
    }

    # Render the individual file view template with the context
    return render(request, "login/individual_file_view_ip.html", context)


def individual_file_view_resolved(request, report_id):
    # Retrieve the corresponding report from the database
    report = get_object_or_404(Report, pk=report_id)
    if report.status != "RESOLVED":
        report.status = "IN PROGRESS"
        report.save()

    # Prepare the context with the details of the specific report
    context = {
        "report": report,
    }

    # Render the individual file view template with the context
    return render(request, "login/individual_file_view_resolved.html", context)


def delete_report(request, report_id):
    if request.user.is_authenticated:
        # Retrieve the report object based on the report_id
        report = get_object_or_404(Report, pk=report_id)
        prevPage = request.GET.get('prevPage', None)

        # Check if the current user is the owner of the report
        if report.attached_user == request.user.username:
            # Delete the file from S3 bucket if it exists
            if report.filenames:
                s3 = boto3.client(
                    "s3",
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                )
                s3.delete_object(Bucket=AWS_STORAGE_BUCKET_NAME, Key=report.filenames)

            # Delete the report from the database
            report.delete()

            # Redirect the user back to their list of reports or a default page
            if prevPage == "user_reports":
                return redirect("login:user_reports")
            elif prevPage == "user_reports_new":
                return redirect("login:user_list_files_new")
            elif prevPage == "user_reports_ip":
                return redirect("login:user_list_files_ip")
            elif prevPage == "user_reports_resolved":
                return redirect("login:user_list_files_resolved")
            else:
                return redirect("login:user_reports")
        else:
            # If the user is not the owner, return an error or redirect to an appropriate page
            return HttpResponse("You are not authorized to delete this report.")
    else:
        # If the user is not authenticated, redirect them to the login page
        return redirect("login")