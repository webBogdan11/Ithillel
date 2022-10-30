from django import forms
from django.contrib.auth import get_user_model


class UserCreationFrom(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('email', )

    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def save(self, *args, **kwargs):
        new_user = super().save(commit=False,)
        email = self.cleaned_data['email']
        new_user.username = email[:email.index('@')]

        new_user.set_password(
            self.cleaned_data['password']
        )
        return new_user