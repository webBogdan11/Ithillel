from django.contrib.auth import login, authenticate
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView as AuthLoginView
from users.forms import RegistrationForm, CustomAuthenticationForm


class CreateUserView(FormView):
    form_class = RegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('products:index')

    def form_valid(self, form):
        login(self.request, form.save(), backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request,
                         f'{get_user_model().objects.get(email=form.cleaned_data["email"])} are successfully registered!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request,
                       f'Incorrect data')
        return super().form_invalid(form)


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
