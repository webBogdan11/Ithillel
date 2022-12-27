import django_filters

from products.models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    price__gt = django_filters.NumberFilter(field_name='price',
                                            lookup_expr='gt')

    class Meta:
        model = Product
        fields = ['price__gt', 'name', 'category', 'currency']
