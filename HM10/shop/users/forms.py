import random

from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, UsernameField, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from users.tasks import send_sms
from shop.helpers import send_html_mail

User = get_user_model()


class RegistrationForm(UserCreationForm):

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = User
        fields = ("email", "phone")
        field_classes = {'email': UsernameField}

    def clean(self):
        self.instance.username = self.cleaned_data['email'].split('@')[0]
        try:
            User.objects.get(username=self.instance.username)
            raise ValidationError("A user with that username already exists.")
        except User.DoesNotExist:
            ...
        self.instance.is_active = False
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)
        context = {
            'email': user.email,
            'domain': settings.DOMAIN,
            'site_name': 'SHOP',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'subject': 'Confirm registration'
        }
        subject_template_name = 'emails/registration/registration_confirm_subject.txt'  # noqa
        email_template_name = 'emails/registration/registration_confirm_email.html'  # noqa

        send_html_mail(
            subject_template_name,
            email_template_name,
            from_email=settings.SERVER_EMAIL,
            to_email=user.email,
            context=context
        )

        if self.cleaned_data.get('phone'):
            code = random.randint(10000, 99999)
            cache.set(f'{str(user.id)}_code', code, timeout=60)
            send_sms.delay(self.cleaned_data.get('phone'), code)
            self.request.session['user_id'] = user.id
        return user


class PhoneCodeForm(forms.Form):
    code = forms.IntegerField()

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.user_id = self.request.session.get('user_id', 0)
        self.user = User.objects.get(id=self.user_id)

    def clean_code(self):
        if self.cleaned_data['code'] == cache.get(f'{str(self.user.id)}_code'):
            self.user.is_active = True
            self.user.is_phone_valid = True
            self.user.save(update_fields=('is_active', 'is_phone_valid'))
        else:
            raise ValidationError('Phone code is not correct')


class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}),
                             required=False)
    phone = forms.CharField(required=False)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        phone = self.cleaned_data.get('phone')

        if not username and not phone:
            raise ValidationError('Email or phone number is required.')

        if password:
            kwargs = {'password': password, 'username': username}
            if phone and not username:
                kwargs.pop('username')
                kwargs.update({'phone': phone})
            self.user_cache = authenticate(self.request, **kwargs)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data
