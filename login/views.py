from django.shortcuts import render
from django.contrib.auth import logout


def auth_home(request):
    return render(request=request, template_name="login/auth_home.html", context={})


def home(request):
    return render(request=request, template_name="login/home.html", context={})


def logout_view(request):
    logout(request)
    return render(request, template_name="login/logout.html")
