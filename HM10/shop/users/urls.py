from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as users_views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', users_views.CreateUserView.as_view(), name='register'),
]
