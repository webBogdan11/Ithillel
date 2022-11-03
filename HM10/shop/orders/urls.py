from django.urls import path, re_path
from orders import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    re_path(r'cart/(?P<action>add|remove)/',
            views.UpdateCartView.as_view(),
            name='update_cart'),
    path('recalculate/', views.RecalculateCartView.as_view(),
         name='recalculate_cart'),
    path('purchase/', views.PurchaseView.as_view(),
         name='purchase'),
]
