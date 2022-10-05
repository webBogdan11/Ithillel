from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=250)
    image = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Category(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=250)
    image = models.ImageField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Product(models.Model):
    price = models.PositiveIntegerField()
    sku = models.CharField(max_length=25)


class Discount(models.Model):
    DISCOUNT_TYPE_CHOICES = (
        (0, 'В деньгах'),
        (1, 'Проценты'),
    )
    amount = models.PositiveIntegerField()
    code = models.CharField(max_length=25)
    is_active = models.BooleanField(default=True)
    discount_type = models.CharField(max_length=10,
                                     choices=DISCOUNT_TYPE_CHOICES)

