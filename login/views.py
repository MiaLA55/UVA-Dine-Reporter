from django.shortcuts import render


def auth_home(request):
    return render(request=request, template_name="login/auth_home.html", context={})


def home(request):
    return render(request=request, template_name="login/home.html", context={})
