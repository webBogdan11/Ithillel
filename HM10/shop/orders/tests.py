from django.urls import reverse
from products.models import Product
from orders.models import Order


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


def test_order_update_remove_cart_view(login_user, faker, products):
    url_add = reverse('orders:update_cart', args=('add',))

    client, user = login_user

    product_one_id = Product.objects.get(name='Product1').id
    product_two_id = Product.objects.get(name='Product2').id
    product_three_id = Product.objects.get(name='Product3').id

    response = client.post(url_add, data={'product': product_one_id})
    assert response.status_code == 302

    response = client.post(url_add, data={'product': product_two_id})
    assert response.status_code == 302

    response = client.post(url_add, data={'product': product_three_id})
    assert response.status_code == 302

    assert Order.objects.get(user=user).products.count() == 3

    # Remove products from card
    url_remove = reverse('orders:update_cart', args=('remove',))

    response = client.post(url_remove, data={'product': product_two_id})
    assert response.status_code == 302

    response = client.post(url_remove, data={'product': product_three_id})
    assert response.status_code == 302

    assert Order.objects.get(user=user).products.count() == 1



