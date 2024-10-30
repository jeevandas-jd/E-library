# library_app/forms.py
from django import forms

class FileUploadForm(forms.Form):
    file = forms.FileField()
    destination_name = forms.CharField(max_length=255, help_text="Path within the bucket where the file will be stored.")
