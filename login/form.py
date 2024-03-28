from django import forms


class FileUploadForm(forms.Form):
    filename = forms.CharField(widge=forms.HiddenInput())
