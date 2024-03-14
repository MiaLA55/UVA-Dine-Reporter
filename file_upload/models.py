from django.db import models

class Report(models.Model):
    report_explanation = models.TextField(blank=True, null=True)
    file_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name