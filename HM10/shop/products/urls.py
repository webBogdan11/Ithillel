from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('products_list/', views.ProductsView.as_view(), name='products_list'),
    path('products_detail/<uuid:pk>', views.ProductsDetail.as_view(), name='products_detail'),
    path('products/export_csv/', views.export_csv, name='export_csv'),
    path('products/import_csv/', views.ImportCSV.as_view(), name='import_csv'),
    path('products/parse', views.parse_products_view, name='parse'),

]
