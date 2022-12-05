from django.urls import reverse


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


