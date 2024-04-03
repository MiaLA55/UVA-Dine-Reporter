from django.db import models
from datetime import datetime


class ReportResponse(models.Model):
    response = models.CharField(max_length=2048)
    report_filename = models.CharField(max_length=2048)


class Report(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('IN PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    report_response = models.OneToOneField('ReportResponse', on_delete=models.SET_NULL, null=True, blank=True)
    explanation = models.TextField()
    filenames = models.CharField(max_length=2048)
    attached_user = models.CharField(max_length=500, default='Anonymous')
    resolved_notes = models.TextField(blank=True)
    created_datetime = models.DateTimeField(default=datetime.now)