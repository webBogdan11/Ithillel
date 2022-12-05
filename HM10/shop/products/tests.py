from django.urls import reverse
from django.core import mail
from products.models import Product


def test_index_view(client, faker):
    response = client.get(reverse('products:index'))
    assert response.status_code == 200
    assert b'Your best friend is here' in response.content

    data = {
         'email': faker.word(),
         'text': faker.sentence()
     }
    response = client.post(reverse('products:index'), data=data)
    assert response.status_code == 200
    assert not len(mail.outbox)

    data = {
         'email': faker.email(),
         'text': faker.sentence()
     }
    response = client.post(reverse('products:index'), data=data, follow=True)
    assert response.status_code == 200
    assert any(i[0] == reverse('products:index') for i in response.redirect_chain)
    assert data['email'] in mail.outbox[0].body
    assert data['text'] in mail.outbox[0].body


def test_product_list_and_detail_view(client, products, faker):
    products_all = Product.objects.all()

    response = client.get(reverse('products:products_list'))
    assert response.status_code == 200
    assert response.template_name[0] == 'products/products_list.html'
    assert len(response.context['products']) == 3

    response = client.get(reverse('products:products_detail', args=(str(products_all[0].id),)))
    assert response.status_code == 200

    response = client.get(reverse('products:products_detail', args=(faker.uuid4(),)))
    assert response.status_code == 404

