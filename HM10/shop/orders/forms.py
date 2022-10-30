from django import forms
from orders.models import Discount
from django.core.exceptions import ValidationError


class DiscountApply(forms.Form):
    code = forms.CharField(max_length=10)

    def clean_code(self):
        code = Discount.objects.filter(code=self.cleaned_data['code']).first()
        if code:
            return code
        else:
            raise ValidationError(f"There is no discount "
                                  f"with this code {self.cleaned_data['code']}")

