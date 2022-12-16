from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as users_views

app_name = 'users'

urlpatterns = [
    path('login/', users_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', users_views.CreateUserView.as_view(), name='register'),
    path('registration/<uidb64>/<token>/confirm/',
         users_views.RegistrationConfirmView.as_view(),
         name='registration_confirm'),
    path('phone/confirm', users_views.PhoneEntering.as_view(), name='phone')
]
