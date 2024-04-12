from django import forms
from .models import Report, Tag

class TagSelectionForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.CheckboxSelectMultiple)

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['explanation', 'filenames']
