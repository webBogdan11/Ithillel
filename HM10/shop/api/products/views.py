from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django_filters import rest_framework as filters
from api.products.serializers import ProductSerializer, CategorySerializer
from products.models import Product, Category
from api.products.filters import ProductApiFilter


class ProductsViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductApiFilter


class CategoryViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='products',
            serializer_class=ProductSerializer)
    def get_products(self, request, *args, **kwargs):
        """
        /api/v1/categories/:id/products/
        :param request:
        :return:
        """
        serializer = self.get_serializer(self.get_object().product_set,
                                         many=True)
        return Response(serializer.data)
