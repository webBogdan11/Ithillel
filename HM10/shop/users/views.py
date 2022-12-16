from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import RedirectView
from django.contrib.auth.views import LoginView as AuthLoginView
from django.contrib.auth import get_user_model
from users.forms import RegistrationForm, CustomAuthenticationForm, PhoneCodeForm


User = get_user_model()


class CreateUserView(FormView):
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:phone')

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(request=self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       f'Incorrect data')
        return super().form_invalid(form)


class PhoneEntering(FormView):
    form_class = PhoneCodeForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def get_form(self, form_class=None):
        """Return an instance of the form to be used in this view."""
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(request=self.request, **self.get_form_kwargs())

    def form_valid(self, form):
        messages.success(self.request,
                         f'Welcome {form.user.email}! Pls log in')
        return HttpResponseRedirect(self.get_success_url())


class LoginView(AuthLoginView):
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        messages.success(self.request,
                         f'Welcome back {form.get_user().email}!')

        login(self.request, form.get_user(), backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        messages.error(self.request,
                       f'Incorrect data')
        return super().form_invalid(form)


class RegistrationConfirmView(RedirectView):
    url = reverse_lazy('users:login')

    def get(self, request, *args, **kwargs):
        user = self.get_user(kwargs['uidb64'])

        if user is not None:
            token = kwargs['token']
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save(update_fields=('is_active',))
                messages.success(
                    request,
                    'Activation success. '
                    'You can login using your email and password.'
                )
            else:
                messages.error(request, 'Activation error.')
        return super().get(request, *args, **kwargs)

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist,
                ValidationError):
            user = None
        return user
