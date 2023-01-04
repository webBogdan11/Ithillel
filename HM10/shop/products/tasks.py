import decimal
import io

from django.core.files.images import ImageFile
from django.core.mail import send_mail
from shop.celery import app
# from products.models import Config
from shop.settings import EMAIL_HOST_USER
from shop.api_clients import BaseClient
from products.models import Category, Product
from products.client.client import citrus_parser

# email_config = Config.load()


@app.task
def send_contact_form(email, text):
    send_mail(
        'Message from client',
        f'From {email} Message: {text}',
        from_email=EMAIL_HOST_USER,
        # recipient_list=[email_config.contact_form_email],
    )


@app.task
def save_parsed_products(products_list: list):
    if not products_list:
        return
    request_client = BaseClient()
    for product_dict in products_list:
        category, _ = Category.objects.get_or_create(
            name=product_dict['category']
        )
        try:
            response = request_client.get_request(
                url=product_dict['image'],
                method='get'
            )
        except Exception as err:
            continue
        image = ImageFile(io.BytesIO(response), name='image.jpg')
        price = decimal.Decimal(
            ''.join(i for i in product_dict['price'] if i.isdigit())
        )
        product, created = Product.objects.get_or_create(
            name=product_dict['name'],
            category=category,
            defaults={
                'image': image,
                'description': product_dict['description'],
                'price': price
            }
        )
        if not created:
            product.price = price
            product.image = image
            product.save(update_fields=('price', 'image'))


@app.task
def parse_products():
    save_parsed_products.delay(citrus_parser.parse())
