from django import forms
from orders.models import Discount
from django.core.exceptions import ValidationError

from products.models import Product


class DiscountApply(forms.Form):
    code = forms.CharField(max_length=10)

    def clean_code(self):
        code = Discount.objects.filter(code=self.cleaned_data['code']).first()
        if code:
            return code
        else:
            raise ValidationError(f"There is no discount "
                                  f"with this code {self.cleaned_data['code']}")


class UpdateCartOrderForm(forms.Form):
    product = forms.UUIDField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.instance = kwargs['instance']

    def clean_product_id(self):
        try:
            product = Product.objects.get(id=self.cleaned_data['product'])
        except Product.DoesNotExist:
            raise ValidationError('Wrong product id.')
        return product

    def save(self, action):
        getattr(self.instance.products, action)(self.cleaned_data['product'])


class RecalculateCartForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.instance = kwargs['instance']
        self.fields = {k: forms.IntegerField() if k.startswith(
            'quantity') else forms.UUIDField() for k in self.data.keys() if
                       k != 'csrfmiddlewaretoken'}

    def save(self):
        """
        {'quantity_0': 2,
        'product_0': UUID('e04bc1aa-dc11-4791-a187-5118ea5ce01a'),
        'quantity_1': 2,
        'product_1': UUID('4e26895f-2056-4c57-ad53-3a09c9861b56'),
        'quantity_2': 3,
        'product_2': UUID('f6177123-adb7-4237-bc3e-8a5d2aabae6e')}
        :return: instance
        """
        for k in self.cleaned_data.keys():
            if k.startswith('product_'):
                index = k.split('_')[-1]
                self.instance.products.through.objects \
                    .filter(product_id=self.cleaned_data[f'product_{index}']) \
                    .update(quantity=self.cleaned_data[f'quantity_{index}'])
        return self.instance
