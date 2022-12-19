from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from api.user_api.serializers import UsersSerializer

from feedback.models import Feedback

User = get_user_model()


class FeedbackSerializer(serializers.ModelSerializer):
    user = UsersSerializer(required=False, allow_null=False)

    class Meta:
        model = Feedback
        fields = ('id', 'text', 'rating', 'user')

    def validate_text(self, value):
        if 'http' in value:
            raise ValidationError("The 'text' field must not contains urls.")
        return value

    def create(self, validated_data):
        validated_data.update({'user': self.context['request'].user})
        instance = super().create(validated_data)
        return instance
