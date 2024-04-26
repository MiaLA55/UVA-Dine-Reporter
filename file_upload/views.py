from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ReportForm, TagSelectionForm
from .models import Tag

def upload_page(request):
    return HttpResponse("Uploading")


def user_submit_report(request):
    report_form = ReportForm()
    tag_selection_form = TagSelectionForm()
    available_tags = Tag.objects.all()

    return render(request, 'file_upload/user_submit_report.html', {'report_form': report_form, 'tag_selection_form': tag_selection_form, 'available_tags': available_tags})



def success(request):
    return render(request, 'file_upload/success.html')
#