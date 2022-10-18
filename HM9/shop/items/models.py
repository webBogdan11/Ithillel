from django.db import models
from os import path
from django.core.validators import MinValueValidator
from shop.mixins.models_mixins import PKMixin


def upload_image(instance, filename):
    _name, extension = path.splitext(filename)
    return f'images/{instance.__class__.__name__.lower()}/' \
           f'{instance.pk}/image{extension}'


class Category(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to=upload_image)

    def __str__(self):
        return self.name


class Item(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        "items.Category",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.name} | {self.category}'


class Product(PKMixin):
    name = models.CharField(max_length=255)
    price = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    sku = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f'{self.name} | {self.price} | {self.sku}'
