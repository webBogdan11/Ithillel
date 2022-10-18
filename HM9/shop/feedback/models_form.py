from django import forms
from feedback.models import Feedback
from django.utils.html import strip_tags


class FeedbackModelForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('text', 'user', 'rating')

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['user'].initial = user

    def clean_text(self):
        text = self.cleaned_data['text']
        allowed_special_symbols = (' ', '.', ',')
        new_text = ''.join([i if i.isalnum() or i in allowed_special_symbols
                            else '' for i in strip_tags(text)])
        return new_text
