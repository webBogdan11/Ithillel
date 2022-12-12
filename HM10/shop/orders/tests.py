from decimal import Decimal

from django.urls import reverse
from orders.models import Order
from orders.tasks import send_to_console_task


def test_order_redirect(client):
    response = client.get(reverse('orders:cart'), follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('users:login') + '?next=' + reverse('orders:cart')

    response = client.get(reverse('orders:update_cart', args=('add',)), follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('users:login') + '?next=' + reverse('orders:update_cart',
                                                                                        args=('add',))

    response = client.get(reverse('orders:update_cart', args=('remove',)), follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('users:login') + '?next=' + reverse('orders:update_cart',
                                                                                        args=('remove',))

    response = client.get(reverse('orders:recalculate_cart'), follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('users:login') + '?next=' + reverse('orders:recalculate_cart')

    response = client.get(reverse('orders:purchase'), follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('users:login') + '?next=' + reverse('orders:purchase')


def test_order_cart_view(login_user, faker):
    url = reverse('orders:cart')

    client, user = login_user

    response = client.get(url)

    assert response.status_code == 200


def test_order_update_remove_cart_view(mocker, login_user, faker, product_factory, discount_factory):
    url_add = reverse('orders:update_cart', args=('add',))

    client, user = login_user

    product_one = product_factory(price=Decimal(250))
    product_two = product_factory(price=Decimal(200))
    product_three = product_factory(price=Decimal(300))

    # Add products from card

    response = client.post(url_add, data={'product': product_one.id})
    assert response.status_code == 302

    response = client.post(url_add, data={'product': product_two.id})
    assert response.status_code == 302

    response = client.post(url_add, data={'product': product_three.id})
    assert response.status_code == 302

    response = client.post(url_add, data={'product': faker.uuid4()})
    assert response.status_code == 302

    order1 = Order.objects.get(user=user)

    assert order1.products.count() == 3
    assert order1.total_amount == 750

    # Recalculate Test
    recalculate_url = reverse('orders:recalculate_cart')

    data = {'quantity_0': 1,
            'product_0': product_one.id,
            'quantity_1': 2,
            'product_1': product_two.id,
            'quantity_2': 3,
            'product_2': product_three.id}

    response = client.post(recalculate_url, data=data)
    order1 = Order.objects.get(user=user)

    assert response.status_code == 302
    assert order1.total_amount == 1550

    # Apply Discount
    url_discount = reverse('orders:apply_discount')

    response = client.post(url_discount, data={'code': faker.name()})
    assert response.status_code == 302

    discount = discount_factory(discount_type=0, amount=200)

    response = client.post(url_discount, data={'code': discount.code})
    order1 = Order.objects.get(user=user)

    assert response.status_code == 302
    assert order1.total_amount == 1350

    # Remove products from card
    url_remove = reverse('orders:update_cart', args=('remove',))

    response = client.post(url_remove, data={'product': product_two.id})
    assert response.status_code == 302

    response = client.post(url_remove, data={'product': faker.uuid4()})
    assert response.status_code == 302

    response = client.post(url_remove, data={'product': product_three.id})
    assert response.status_code == 302

    order1 = Order.objects.get(user=user)
    assert order1.products.count() == 1
    assert order1.total_amount == 50

    # Order purchase

    purchase_url = reverse('orders:purchase')
    mocker.patch("orders.views.send_to_console_task.delay", return_value=1)
    response = client.post(purchase_url)

    order1 = Order.objects.get(user=user)
    assert response.status_code == 200
    assert order1.is_active is False
    assert order1.is_paid is True


def test_cart_discount_calculate(order_factory, product_factory, discount_factory):
    product1 = product_factory(price=Decimal(100))
    product2 = product_factory(price=Decimal(200))
    product3 = product_factory(price=Decimal(300))

    discount1 = discount_factory(discount_type=0, amount=200)

    order1 = order_factory(discount=discount1, post_create=[product1, product2, product3])

    assert order1.total_amount == 400

    discount1 = discount_factory(discount_type=1, amount=10)
    order1 = order_factory(discount=discount1, post_create=[product1, product2, product3])

    assert order1.total_amount == 540



