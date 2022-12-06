import pytest
from faker import Faker
from products.models import Product, Category
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test.client import Client

fake = Faker()
User = get_user_model()


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


@pytest.fixture(scope='function')
def user(db):
    user, _ = User.objects.get_or_create(
        email='user@user.com',
        username='user',
        first_name='John Smith',
        phone='123456789',
        is_phone_valid=True
    )
    user.set_password('123456789')
    user.save()
    yield user


@pytest.fixture(scope='function')
def login_user(db):
    phone = '123456789'
    password = '123456789'
    user, _ = User.objects.get_or_create(
        email='user@user.com',
        username='user',
        first_name='John Smith',
        phone=phone,
        is_phone_valid=True
    )
    user.set_password(password)
    user.save()
    client = Client()
    response = client.post(reverse('users:login'),
                           data={'phone': phone,
                                 'password': password})
    assert response.status_code == 302
    yield client, user
