from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api.feedback.serializers import FeedbackSerializer
from feedback.models import Feedback


class FeedbacksViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.select_related('user')
        return queryset
