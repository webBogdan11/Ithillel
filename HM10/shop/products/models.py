from os import path
from django.db import models

from shop import settings
from shop.mixins.models_mixins import PKMixin
from shop.constants import MAX_DIGITS, DECIMAL_PLACES


def upload_image(instance, filename):
    _name, extension = path.splitext(filename)
    return f'images/{instance.__class__.__name__.lower()}/' \
           f'{instance.pk}/image{extension}'


class Category(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image,
                              blank=True)

    def __str__(self):
        return self.name


class Product(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image,
                              default='images/product/no_food',
                              blank=True,
                              null=True,)
    category = models.ForeignKey(
        "products.Category",
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    sku = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    products = models.ManyToManyField('products.Product', blank=True)

    def __str__(self):
        return f'{self.name} | {self.price} | {self.sku}'
