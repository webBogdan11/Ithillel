from django.urls import reverse
from products.models import Product
from favorite.models import Favorite


def test_favorite_view(login_user, client, faker):
    url = reverse('favorite:favorite_list')

    response = client.get(url, follow=True)

    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('users:login') + '?next=' + url

    client, user = login_user

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name[0] == 'favorite/favorite_list.html'


def test_save_remove_favorite_view(login_user, client, faker, products):
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

    product_one_id = Product.objects.get(name='Product1').id
    product_two_id = Product.objects.get(name='Product2').id
    product_three_id = Product.objects.get(name='Product3').id

    data = {
        'user': str(user.id),
        'product': product_one_id
    }

    assert not Favorite.objects.exists()

    response = client.post(url_save, data=data)
    assert response.status_code == 302

    data['product'] = product_two_id
    response = client.post(url_save, data=data)
    assert response.status_code == 302

    data['product'] = product_three_id
    response = client.post(url_save, data=data)
    assert response.status_code == 302

    assert Favorite.objects.exists()
    assert Favorite.objects.count() == 3

    # Test remove Favorite product

    response = client.post(url_remove, data=data)
    assert response.status_code == 302

    data['product'] = product_two_id

    response = client.post(url_remove, data=data)
    assert response.status_code == 302

    assert Favorite.objects.count() == 1


