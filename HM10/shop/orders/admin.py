from django.contrib import admin

from orders.models import Order, Discount


@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('products',)


admin.site.register(Discount)
