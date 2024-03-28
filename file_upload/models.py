from django.db import models


class ReportResponse(models.Model):
    response = models.CharField(max_length=2048)
    report_filename = models.CharField(max_length=2048)
