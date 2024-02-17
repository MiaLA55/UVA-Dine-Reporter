from django.shortcuts import render


def login(request):
    return render(request=request, template_name='login/login.html', context={})
