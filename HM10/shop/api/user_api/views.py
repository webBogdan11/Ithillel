from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.user_api.serializers import UsersSerializer, FavoriteSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='favorite_products',
            serializer_class=FavoriteSerializer)
    def get_products(self, request, *args, **kwargs):
        """
        /api/v1/categories/:id/products/
        :param request:
        :return:
        """
        serializer = self.get_serializer(self.get_object().favorites,
                                         many=True)
        return Response(serializer.data)
