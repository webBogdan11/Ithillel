from django.urls import path, re_path
from favorite import views

app_name = 'favorite'

urlpatterns = [
    path('favorite_list/', views.FavoriteView.as_view(), name='favorite_list'),
    re_path(r'favorite/(?P<action>save|remove)/',
            views.UpdateFavoriteView.as_view(),
            name='update_favorite'),
]
