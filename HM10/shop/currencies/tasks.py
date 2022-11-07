import logging
from datetime import timedelta
from currencies.models import CurrencyHistory
from django.utils import timezone
from celery import shared_task
from shop.model_choices import Currency
from currencies.clients.clients import privat_currency_client, mono_bank_client
from shop.celery import app


logger = logging.getLogger(__name__)


@app.task
def clear_old_currencies():
    CurrencyHistory.objects.filter(
        created_at__lt=timezone.now() - timedelta(days=3),
    ).delete()


@shared_task
def get_currencies():
    try:
        currency_list = mono_bank_client.get_currency()
    except Exception as err:
        logger.error(err)
        currency_list = privat_currency_client.get_currency()

    currency_history_list = []
    for currency in currency_list:
        try:
            if currency['ccy'] in [i.value for i in Currency]:
                currency_history_list.append(
                    CurrencyHistory(
                        currency=currency['ccy'],
                        buy=currency['buy'],
                        sale=currency['sale']
                    )
                )
        except (KeyError, ValueError) as err:
            logger.error(err)

    if currency_history_list:
        CurrencyHistory.objects.bulk_create(currency_history_list)
        clear_old_currencies.delay()
