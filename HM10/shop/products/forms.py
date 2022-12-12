import csv
import decimal
from io import StringIO

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from products.models import Product, Category


class CsvImport(forms.Form):
    file = forms.FileField(
        validators=[FileExtensionValidator(['csv'])]
    )


class ImportCSVForm(forms.Form):
    file = forms.FileField(
        validators=[FileExtensionValidator(['csv'])]
    )

    def clean_file(self):
        csv_file = self.cleaned_data['file']
        reader = csv.DictReader(StringIO(csv_file.read().decode('utf-8')))

        products_list = []
        for product in reader:
            try:
                products_list.append(
                    Product(
                        name=product['name'],
                        description=product['description'],
                        price=decimal.Decimal(product['price']),
                        sku=product['sku'],
                        category=Category.objects.get_or_create(
                            name=product['category']
                        )[0]
                    )
                )
            except (KeyError, decimal.InvalidOperation) as err:
                raise ValidationError(err)
        if not products_list:
            raise ValidationError('Wrong file format.')
        return products_list

    def save(self):
        products_list = self.cleaned_data['file']
        Product.objects.bulk_create(products_list)


class ContactForm(forms.Form):
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)
