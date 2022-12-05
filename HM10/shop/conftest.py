import pytest
from faker import Faker
from products.models import Product, Category

fake = Faker()


@pytest.fixture(scope='session')
def faker():
    # global fake
    yield fake


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    from pprint import pp
    __builtins__['pp'] = pp
    # code before tests run
    yield
    del __builtins__['pp']
    # code after tests run


@pytest.fixture(scope='function')
def products(db):
    categories = [
        Category(name='Category1'),
        Category(name='Category2')
    ]
    Category.objects.bulk_create(categories)

    products = [
        Product(name='Product1', category=categories[0]),
        Product(name='Product2', category=categories[0]),
        Product(name='Product3', category=categories[1]),
    ]

    Product.objects.bulk_create(products)
    return
