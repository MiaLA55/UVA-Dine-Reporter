from django import forms


# class FileUploadForm(forms.Form):
#     filename = forms.CharField(widge=forms.HiddenInput())

class ResolveReportForm(forms.Form):
    report_name = forms.CharField(label="Report Name", max_length=100)
    resolve_notes = forms.CharField(label="Resolve Notes", widget=forms.Textarea)
