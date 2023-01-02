from django.db import models
from products.models import Product
from django.contrib.auth import get_user_model


class Favorite(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='favorites')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='favorites')

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self): # pragma: no cover
        return f'{self.user} -- {self.product}'
