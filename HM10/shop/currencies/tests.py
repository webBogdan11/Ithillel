from currencies.models import CurrencyHistory
from currencies.tasks import get_currencies
import pytest


def test_get_mono_currencies_task(mocker, faker):
    assert not CurrencyHistory.objects.exists()
    get_currency = mocker.patch('currencies.clients.clients.mono_bank_client.get_currency')
    get_currency.return_value = [
         {'ccy': 'USD', 'buy': '2', 'sale': '3'},
         {'ccy': 'EUR', 'buy': '4', 'sale': '5'},
     ]
    assert not get_currency.call_count

    get_currencies()

    assert get_currency.call_count
    assert CurrencyHistory.objects.filter(currency='USD', sale='3')
    assert CurrencyHistory.objects.filter(currency='EUR', sale='5')


def test_get_privat_currencies_task(mocker, faker):
    assert not CurrencyHistory.objects.exists()
    mono_get_currency = mocker.patch('currencies.clients.clients.mono_bank_client.get_currency')
    mono_get_currency.side_effect = Exception
    privat_get_currency = mocker.patch('currencies.clients.clients.privat_currency_client.get_currency')
    privat_get_currency.return_value = [
        {'ccy': 'USD', 'buy': '2', 'sale': '3'},
        {'ccy': 'EUR', 'buy': '4', 'sale': '5'},
    ]
    assert not privat_get_currency.call_count

    get_currencies()

    assert privat_get_currency.call_count
    assert CurrencyHistory.objects.filter(currency='USD', sale='3')
    assert CurrencyHistory.objects.filter(currency='EUR', sale='5')

    time_created_at = CurrencyHistory.objects.get(currency='EUR', sale='5').created_at
    assert str(CurrencyHistory.objects.get(currency='EUR', sale='5')) == f'EUR 5.00 {time_created_at}'


def test_get_currencies_incorrect_api_output(mocker, faker):
    assert not CurrencyHistory.objects.exists()
    get_currency = mocker.patch('currencies.clients.clients.mono_bank_client.get_currency')
    logger = mocker.patch('currencies.tasks.logger.error')
    get_currency.return_value = [
         {'cci': 'USD', 'buy': '2', 'sale': '3'},
         {'cci': 'EUR', 'buy': '4', 'sale': '5'},
     ]
    logger.return_value = 'Error message'
    assert not get_currency.call_count
    assert not logger.call_count

    get_currencies()

    assert get_currency.call_count
    assert logger.call_count
