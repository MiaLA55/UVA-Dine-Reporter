from django.db import models
from django.utils import timezone


class ReportResponse(models.Model):
    response = models.CharField(max_length=2048)
    report_filename = models.CharField(max_length=2048)


class Report(models.Model):
    STATUS_CHOICES = (
        ("NEW", "New"),
        ("IN PROGRESS", "In Progress"),
        ("RESOLVED", "Resolved"),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="NEW")
    explanation = models.TextField(default=None, null=True, blank=True)
    filenames = models.CharField(max_length=2048, default=None, null=True, blank=True)
    attached_user = models.CharField(max_length=200)
    resolved_notes = models.TextField(blank=True, null=True)
    submission_time = models.DateTimeField(default=timezone.now)
    id = models.AutoField(primary_key=True)
