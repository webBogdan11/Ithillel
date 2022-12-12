import pytest
import factory
import random
from faker import Faker
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test.client import Client
from pytest_factoryboy import register
from orders.models import Order, OrderProductRelation, Discount
from products.models import Product, Category
from shop.constants import DECIMAL_PLACES

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
def user_usual(db):
    password = '123456789'
    data = {
        'email': 'user@user.com',
        'username': 'user',
        'first_name': 'John Smith',
        'phone': '123456789',
        'is_phone_valid': True
    }
    user = UserFactory(**data)
    user.set_password(password)
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


@register
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('email',)

    email = factory.Sequence(lambda x: fake.email())
    first_name = factory.Sequence(lambda x: fake.name())
    last_name = factory.Sequence(lambda x: fake.name())


@register
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda x: fake.name())
    description = factory.Sequence(lambda x: fake.name())
    image = factory.django.ImageField()


@register
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
        django_get_or_create = ('name', 'category')

    name = factory.Sequence(lambda x: fake.name())
    description = factory.Sequence(lambda x: fake.name())
    image = factory.django.ImageField()
    price = factory.Sequence(lambda x: fake.pydecimal(
        min_value=1,
        left_digits=DECIMAL_PLACES,
        right_digits=DECIMAL_PLACES,
    ))
    sku = factory.Sequence(lambda x: fake.word())
    category = factory.SubFactory(CategoryFactory)

    @factory.post_generation
    def post_create(self, created, *args, **kwargs):
        if created and not kwargs.get('deny_post'):
            for _ in range(1, 5):
                self.products.add(
                    ProductFactory(post_create__deny_post=True)
                )


@register
class DiscountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Discount
        django_get_or_create = ('code',)

    code = factory.Sequence(lambda x: fake.pystr(min_chars=4, max_chars=10))
    discount_type = factory.Sequence(lambda x: random.choice((0, 1)))
    amount = factory.Sequence(lambda x: fake.pydecimal(
        min_value=1,
        left_digits=DECIMAL_PLACES,
        right_digits=DECIMAL_PLACES,
    ))


@register
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    discount = factory.SubFactory(DiscountFactory)

    @factory.post_generation
    def post_create(self, created, extracted, **kwargs):

        if created and extracted:
            for product in extracted:
                self.products.add(product)

        elif created:
            for _ in range(1, 5):
                self.products.add(
                    ProductFactory()
                )


register(OrderFactory, "numbered_order", post_create__deny_post=True)


@register
class OrderProductRelationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderProductRelation
        django_get_or_create = ('order', 'product',)

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Sequence(lambda x: fake.pyint(min_value=1, max_value=8))
