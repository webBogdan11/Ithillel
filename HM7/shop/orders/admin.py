from django.contrib import admin

from orders.models import Order, Discount

admin.site.register(Order)
admin.site.register(Discount)

