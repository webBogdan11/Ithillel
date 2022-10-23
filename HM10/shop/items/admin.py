# from django.contrib import admin
# from items.models import Product, Category, Item
# from shop.mixins.admin_mixins import ImageSnapshotAdminMixin
#
#
# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     filter_horizontal = ('items',)
#     list_display = ('name', 'price', 'sku', 'created_at')
#     list_filter = ('price',)
#     readonly_fields = ('id',)
#
#
# @admin.register(Category)
# class CategoryAdmin(ImageSnapshotAdminMixin, admin.ModelAdmin):
#     pass
#
#
# admin.site.register(Item)
