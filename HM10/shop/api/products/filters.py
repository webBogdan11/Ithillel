from django_filters import rest_framework as filters

from products.models import Product


class ProductApiFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    price__gt = filters.NumberFilter(field_name='price',
                                     lookup_expr='gt')

    class Meta:
        model = Product
        fields = ['price__gt', 'name', 'category', 'currency']
