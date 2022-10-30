from django.urls import path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('orders_form/', views.OrderForm.as_view(), name='orders_form'),
    path('products/add_product/<uuid:pk>', views.order_add_product, name='add_to_order'),
    path('orders/apply_code', views.order_apply_discount, name='apply_discount'),
    path('orders/make_purchase', views.order_make_payment, name='make_purchase'),
]
