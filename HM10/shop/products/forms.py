from django import forms
from django.core.validators import FileExtensionValidator


class CsvImport(forms.Form):
    file = forms.FileField(
        validators=[FileExtensionValidator(['csv'])]
    )
