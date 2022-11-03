from django.db import models
from django.contrib.auth import get_user_model

from shop.constants import MAX_DIGITS, DECIMAL_PLACES

from shop.mixins.models_mixins import PKMixin
from shop.model_choices import DiscountTypes
from django.db.models import Case, When, Sum, F
from django_lifecycle import LifecycleModelMixin, hook, AFTER_UPDATE, BEFORE_UPDATE


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
    products = models.ManyToManyField(
        "products.Product",
        through='orders.OrderProductRelation',
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'],
                                    condition=models.Q(is_active=True),
                                    name='unique_is_active')
        ]

    @property
    def is_current_order(self):
        return self.is_active and not self.is_paid

    def get_total_amount(self):
        return self.products.through.objects.filter(order=self).annotate(
            full_price=F('product__price') * F('quantity')
        ).aggregate(
            total_amount=Case(
                When(
                    order__discount__discount_type=DiscountTypes.VALUE,
                    then=Sum('full_price') - F('order__discount__amount')
                ),
                When(
                    order__discount__discount_type=DiscountTypes.PERCENT,
                    then=Sum('full_price') - (
                            Sum('full_price'
                                ) * F('order__discount__amount') / 100
                    )
                ),
                default=Sum('full_price'),
                output_field=models.DecimalField()
            )
        ).get('total_amount') or 0

    def pay(self):
        self.is_paid = True
        self.save()

    @hook(AFTER_UPDATE)
    def order_after_update(self):
        if self.products.exists():
            self.total_amount = self.get_total_amount()
            self.save(update_fields=('total_amount',), skip_hooks=True)

    @hook(BEFORE_UPDATE, when='is_paid', has_changed=True, was=False)
    def order_is_paid(self):
        self.is_active = False
        self.save(update_fields=('is_active',), skip_hooks=True)

    def __str__(self):
        return f"{self.user} | {str(self.id)[:5]}"


class OrderProductRelation(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='orders'
    )
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return f"{self.order} | {self.product.name}"
