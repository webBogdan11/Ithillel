from django import forms
from django.core.exceptions import ValidationError
from products.models import Product
from favorite.models import Favorite


class UpdateFavoriteForm(forms.Form):
    product = forms.UUIDField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.user = kwargs['user']

    def clean_product(self):
        try:
            product = Product.objects.get(id=self.cleaned_data['product'])
        except Product.DoesNotExist:
            raise ValidationError('Wrong product id.')
        return product

    def save(self, action):
        if action == 'save':
            if Favorite.objects.filter(user=self.user, product=self.cleaned_data['product']):
                return None
            else:
                favorite_obj = Favorite.objects.create(user=self.user,
                                                       product=self.cleaned_data['product'])
            favorite_obj.save()
        elif action == 'remove':
            Favorite.objects.filter(user=self.user, product=self.cleaned_data['product']).delete()
