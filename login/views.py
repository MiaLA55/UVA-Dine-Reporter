from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
import boto3
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.models import AnonymousUser


# views.py


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
    if request.method == "POST" and request.FILES["file"]:
        file = request.FILES["file"]

        # Save the uploaded file
        with open("path/to/save/" + file.name, "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # Redirect or render success message
        return HttpResponseRedirect("/success/")
    return render(request, "upload.html")
