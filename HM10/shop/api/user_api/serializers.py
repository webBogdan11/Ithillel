from django.contrib.auth import get_user_model
from rest_framework import serializers
from api.products.serializers import ProductSerializer
from favorite.models import Favorite

User = get_user_model()


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(allow_null=False)

    class Meta:
        model = Favorite
        fields = ('product', )


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'email', 'phone')