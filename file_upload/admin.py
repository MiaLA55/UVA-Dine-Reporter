from django.contrib import admin
from .models import ReportResponse, Report, Tag

# Register your models here.
admin.site.register(ReportResponse)
admin.site.register(Report)
admin.site.register(Tag)
