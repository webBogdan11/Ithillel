import decimal

from django.db import models

from shop.constants import MAX_DIGITS, DECIMAL_PLACES
from shop.mixins.models_mixins import PKMixin
from shop.model_choices import Currency


class CurrencyHistory(PKMixin):
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.UAH
    )
    buy = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )
    sale = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=1
    )

    @classmethod
    def last_curs(cls, currency_code, attr='sale') -> decimal.Decimal:
        return getattr(cls.objects.filter(
            currency=currency_code
        ).order_by(
            '-created_at'
        ).first(), attr, decimal.Decimal('1.00'))

    def __str__(self):
        return f'{self.currency} {self.sale} {self.created_at}'
