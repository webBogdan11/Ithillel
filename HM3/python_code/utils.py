import requests
from urllib import parse


def get_currency_rates(source, currency, json_reposnse):
    exchange_rate_purchase = None
    exchange_rate_selling = None

    for exchange_rate_info in json_reposnse['exchangeRate']:
        if exchange_rate_info.get('currency') == currency:
            if source == 'NB':
                exchange_rate_purchase = exchange_rate_info.get('purchaseRateNB')
                exchange_rate_selling = exchange_rate_info.get('saleRateNB')
            elif source == 'PB':
                exchange_rate_purchase = exchange_rate_info.get('purchaseRate')
                exchange_rate_selling = exchange_rate_info.get('saleRate')

    if exchange_rate_purchase is None and exchange_rate_selling is None:
        raise Exception('There are not data')

    return exchange_rate_purchase, exchange_rate_selling


def get_convert_currency(date, base_currency,
                         exchange_currency, source):

    if source not in ('PB', 'NB'):
        return 'Вы не правильно указали параметр source для конвертации'

    query_string = {
        'date': date,
    }
    query = parse.urlencode(query_string)
    response = requests.get('https://api.privatbank.ua/p24api/exchange_rates?json&' + query)
    currency_exchange_dict = response.json()

    base_currency_purchase, base_currency_selling = get_currency_rates(source,
                                                                       base_currency,
                                                                       currency_exchange_dict)

    exchange_rate_purchase, exchange_rate_selling = get_currency_rates(source,
                                                                       exchange_currency,
                                                                       currency_exchange_dict)

    if source == 'NB':
        return f'Курс НБУ на {date} при конвертации {base_currency} в {exchange_currency} - ' \
               f'{exchange_rate_purchase / base_currency_purchase}'
    else:
        return f'Курс ПриватБанка на {date} при конвертации {base_currency} в {exchange_currency}' \
               f' для покупки {exchange_rate_purchase / base_currency_purchase} ' \
               f'и для продажи {exchange_rate_selling / base_currency_selling}'




