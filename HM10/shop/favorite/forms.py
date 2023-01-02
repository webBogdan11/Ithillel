from django import forms
from django.core.exceptions import ValidationError
from products.models import Product
from favorite.models import Favorite
from django.contrib.auth import get_user_model


class UpdateFavoriteForm(forms.Form):
    product = forms.UUIDField(required=True)
    action = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.user = get_user_model().objects.get(id=kwargs['user'].id)

    def clean_product(self):
        try:
            product = Product.objects.get(id=self.cleaned_data['product'])
        except Product.DoesNotExist:
            raise ValidationError('Wrong product id.')
        return product

    def save(self):
        if self.cleaned_data['action'] == 'add':
            if Favorite.objects.filter(user=self.user, product=self.cleaned_data['product']):
                return None
            else:
                favorite_obj = Favorite.objects.create(user=self.user,
                                                       product=self.cleaned_data['product'])
            favorite_obj.save()

        elif self.cleaned_data['action'] == 'remove':
            Favorite.objects.filter(user=self.user, product=self.cleaned_data['product']).delete()
