from django.core.mail import send_mail
from shop.celery import app
from products.models import Config
from shop.settings import EMAIL_HOST_USER

email_config = Config.load()


@app.task
def send_contact_form(email, text):
    send_mail(
        'Message from client',
        f'From {email} Message: {text}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[email_config.contact_form_email],
    )
