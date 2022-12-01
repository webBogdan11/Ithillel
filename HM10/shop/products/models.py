import decimal
from django.core.cache import cache
from os import path
from django.db import models

from shop.mixins.models_mixins import PKMixin
from shop.constants import MAX_DIGITS, DECIMAL_PLACES
from currencies.models import CurrencyHistory
from shop.model_choices import Currency
from shop.mixins.singletone_mixins import SingletonModel


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

    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.UAH
    )

    sku = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    products = models.ManyToManyField('products.Product', blank=True)

    @classmethod
    def _cache_key(cls):
        return 'products'

    @classmethod
    def get_products(cls):
        products = cache.get(cls._cache_key())
        if not products:
            products = Product.objects.all()
            cache.set(cls._cache_key(), products)
        return products

    @property
    def exchange_price(self):
        key = f'exchange_price_{self.id}'
        exchange_price = cache.get(key)
        if not exchange_price:
            exchange_price = round(self.price * self.curs, 2)
            cache.set(key, exchange_price)
        return exchange_price

    @property
    def curs(self) -> decimal.Decimal:
        return CurrencyHistory.last_curs(self.currency)

    def __str__(self):
        return f'{self.name} | {self.price} | {self.sku}'


class Config(SingletonModel):
    contact_form_email = models.EmailField(default="webbogdan11@gmail.com")

