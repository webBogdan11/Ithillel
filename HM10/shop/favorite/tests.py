import pytest
from django.urls import reverse
from favorite.models import Favorite
from django.contrib.messages import get_messages
from django.urls.exceptions import NoReverseMatch


def test_favorite_view(login_user, client, faker):
    url = reverse('favorite:favorite_list')

    response = client.get(url, follow=True)

    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('users:login') + '?next=' + url

    client, user = login_user

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name[0] == 'favorite/favorite_list.html'


def test_save_remove_favorite_view(login_user, client, faker, product_factory):
    # Test without logged user
    url_save = reverse('favorite:update_favorite', args=('save', ))

    response = client.get(url_save, follow=True)

    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('users:login') + '?next=' + url_save

    url_remove = reverse('favorite:update_favorite', args=('remove',))

    response = client.get(url_remove, follow=True)

    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('users:login') + '?next=' + url_remove

    # Test save favorite products
    client, user = login_user

    product_one = product_factory()
    product_two = product_factory()
    product_three = product_factory()

    data = {
        'user': str(user.id),
        'product': product_one.id
    }

    assert not Favorite.objects.exists()

    response = client.post(url_save, data=data)
    assert response.status_code == 302

    data['product'] = product_two.id
    response = client.post(url_save, data=data)
    assert response.status_code == 302

    data['product'] = product_three.id
    response = client.post(url_save, data=data)
    assert response.status_code == 302

    assert Favorite.objects.exists()
    assert Favorite.objects.count() == 3

    # Test adding the same product

    response = client.post(url_save, data=data)

    assert response.status_code == 302
    assert Favorite.objects.count() == 3

    # Test remove Favorite product

    response = client.post(url_remove, data=data)
    assert response.status_code == 302

    data['product'] = product_two.id

    response = client.post(url_remove, data=data)
    assert response.status_code == 302

    assert Favorite.objects.count() == 1


def test_exception_favorite_view(login_user, client, faker):
    # Test adding non existing product

    client, user = login_user

    url_save = reverse('favorite:update_favorite', args=('save',))

    wrong_data = {
        'user': str(user.id),
        'product': faker.uuid4(),
    }

    response = client.post(url_save, data=wrong_data, follow=True)
    messages = [m.message for m in get_messages(response.wsgi_request)]

    assert response.status_code == 200
    assert messages[1] == 'Wrong product id'
    assert response.redirect_chain[0][0] == reverse('products:products_list')

    # Test wrong parameter passing

    with pytest.raises(NoReverseMatch):
        reverse('favorite:update_favorite', args=('foo',))


