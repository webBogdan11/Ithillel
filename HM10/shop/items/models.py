# from django.db import models
# from shop.mixins.models_mixins import PKMixin
# from products.models import Category
#
#
# class Item(PKMixin):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     category = models.ForeignKey(
#         Category,
#         on_delete=models.CASCADE
#     )
#
#     def __str__(self):
#         return f'{self.name} | {self.category}'
