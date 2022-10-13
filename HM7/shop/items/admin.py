from django.contrib import admin # noqa

from items.models import Item, Product, Category

admin.site.register(Item)
admin.site.register(Product)
admin.site.register(Category)
