from shop.api_clients import BaseClient
import logging

logger = logging.getLogger(__name__)


class PrivatBankAPI(BaseClient):  # pragma: no cover
    base_url = 'https://api.privatbank.ua/p24api/pubinfo'

    def get_currency(self) -> dict:
        """
        [
            {
            "ccy":"EUR",
            "base_ccy":"UAH",
            "buy":"19.20000",
            "sale":"20.00000"
            },
            {
            "ccy":"USD",
            "base_ccy":"UAH",
            "buy":"15.50000",
            "sale":"15.85000"
            }
            ]
        :return: dict
        """
        return self._request(
            'get',
            params={'exchange': '', 'coursid': 5, 'json': ''}
        )


class MonoBankAPI(BaseClient):  # pragma: no cover
    base_url = 'https://api.monobank.ua/bank/currency'

    def get_currency(self):
        response = self._request(method='get')
        correct_currencies = (840, 978)
        currency_decoder = {
            840: 'USD',
            978: 'EUR',
        }

        result = []
        for element in response:
            correct_data = {}
            if element['currencyCodeA'] in correct_currencies and element['currencyCodeB'] == 980:
                correct_data['ccy'] = currency_decoder[element['currencyCodeA']]
                correct_data['base_ccy'] = 'UAH'
                correct_data['buy'] = element['rateBuy']
                correct_data['sale'] = element['rateSell']
                result.append(correct_data)
        return result


privat_currency_client = PrivatBankAPI()
mono_bank_client = MonoBankAPI()
