from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
from django.core.cache import cache
from shop.mixins.models_mixins import PKMixin


class Feedback(PKMixin):
    text = models.TextField()
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(
        validators=(MaxValueValidator(5),)
    )

    @classmethod
    def _cache_key(cls):
        return 'feedbacks'

    @classmethod
    def update_feedback_cache(cls):
        feedbacks = cls.objects.all()
        cache.set(cls._cache_key(), feedbacks)

    @classmethod
    def get_feedbacks(cls):
        feedbacks = cache.get(cls._cache_key())

        if not feedbacks:
            feedbacks = Feedback.objects.all()
            cache.set(cls._cache_key(), feedbacks)
        return feedbacks

    def __str__(self):
        return f'{self.text[:10]}'
