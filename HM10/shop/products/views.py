from django.shortcuts import render
from django.views.generic import ListView
from products.models import Product


class ProductsListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/products_list.html'


