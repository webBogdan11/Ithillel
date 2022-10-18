from django.contrib.auth import get_user_model, authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from users.forms import UserCreationFrom


class CreateUserView(CreateView):
    model = get_user_model()
    form_class = UserCreationFrom
    template_name = "users/register.html"

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(
            form.cleaned_data['password']
        )
        new_user.save()

        new_user = authenticate(
            username=new_user.username,
            password=form.cleaned_data['password']
        )

        login(self.request, new_user)

        return HttpResponseRedirect(reverse_lazy('items:index'))
