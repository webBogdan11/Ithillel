from django.urls import reverse


def test_favorite_view(client):
    response = client.get(reverse('favorite:favorite_list'), follow=True)

    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('users:login') + '?next=' + reverse('favorite:favorite_list')


def test_save_remove_favorite_view(client):
    response = client.get(reverse('favorite:update_favorite', args=('save', )), follow=True)

    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('users:login') + '?next=' + reverse('favorite:update_favorite',
                                                                                        args=('save', ))

    response = client.get(reverse('favorite:update_favorite', args=('remove',)), follow=True)

    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('users:login') + '?next=' + reverse('favorite:update_favorite',
                                                                                        args=('remove',))
