from django.db import models
from django.contrib.auth import get_user_model

from shop.constants import MAX_DIGITS, DECIMAL_PLACES

from shop.mixins.models_mixins import PKMixin
from shop.model_choices import DiscountTypes
from django.db.models import Case, When, Sum, F
from django_lifecycle import LifecycleModelMixin, hook, AFTER_UPDATE, AFTER_SAVE


class Discount(PKMixin):
    amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    code = models.CharField(
        max_length=32
    )
    is_active = models.BooleanField(
        default=True
    )
    discount_type = models.PositiveSmallIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.VALUE
    )

    def __str__(self):
        return f"{self.amount} | {self.code} | " \
               f"{DiscountTypes(self.discount_type).label}"


class Order(LifecycleModelMixin, PKMixin):
    total_amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name='order',
        null=True,
        blank=True
    )
    products = models.ManyToManyField("products.Product")
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    def get_total_amount(self):
        return self.products.aggregate(
            total_amount=Case(
                When(
                    order__discount__discount_type=None,
                    then=Sum('price')
                ),
                When(
                    order__discount__discount_type=DiscountTypes.VALUE,
                    then=Sum('price') - F('order__discount__amount')
                ),
                default=Sum('price') - (
                        Sum('price') * F('order__discount__amount') / 100),
                output_field=models.DecimalField()
            )
        ).get('total_amount') or 0

    @hook(AFTER_UPDATE)
    @hook(AFTER_SAVE)
    def order_after_update(self):
        if self.products.exists():
            self.total_amount = self.get_total_amount()
            self.save(update_fields=('total_amount',), skip_hooks=True)

    def __str__(self):
        return f"{self.user}"
