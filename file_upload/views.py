from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def upload_page(request):
    return HttpResponse("Uploading")