import logging

from bs4 import BeautifulSoup
from shop.api_clients import BaseClient

logger = logging.getLogger(__name__)


class Parser(BaseClient):
    base_url = 'https://www.ctrs.com.ua/smartfony/brand-apple/'

    def parse(self) -> list:
        response = self.get_request(
            method='get',
        )
        soup = BeautifulSoup(response, features="html5lib")
        try:
            category_name = soup.find('h1', attrs={'class': "mt16 mb16"}).string
            description = soup.find('div', attrs={'class': 'ovh seotext-0-2-270 card'}).div.p.string
        except (AssertionError, IndexError) as err:
            logger.error(err)
        else:
            products_list = []
            for element in soup.find('div', attrs={'class': 'catalog-facet'}).children:
                if element.div['class'][0] == 'nextPage-0-2-289':
                    continue
                try:
                    name = element.div.find('a')['title']

                    price = element.div.find('div', attrs={'class': "medium fz16 price-0-2-569"}).contents[0]

                    img = element.div.find('div', attrs={'class': 'pt8 pr'}).a.img['src']

                    products_list.append(
                        {
                            'name': name,
                            'description': description,
                            'price': price,
                            'category': category_name,
                            'image': img,
                        }
                    )
                except (AssertionError, KeyError) as err:
                    logger.error(err)
            return products_list


citrus_parser = Parser()
