from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('products_list/', views.ProductsListView.as_view(), name='products_list'),
]
