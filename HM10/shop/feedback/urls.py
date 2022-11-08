from django.urls import path

from feedback import views as feedback_views

app_name = 'feedback'

urlpatterns = [
    path('feedback/', feedback_views.feedbacks, name='feedbacks'),
]
