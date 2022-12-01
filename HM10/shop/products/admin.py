from django.contrib import admin

from products.models import Product, Category, Config
from shop.mixins.admin_mixins import ImageSnapshotAdminMixin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ('products',)
    list_display = ('name', 'price', 'sku', 'created_at')
    list_filter = ('price',)
    readonly_fields = ('id',)


@admin.register(Category)
class CategoryAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
    pass


admin.site.register(Config)
