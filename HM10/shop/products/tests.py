from django.urls import reverse
from django.core import mail
import csv
import os
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


def test_product_list_and_detail_view(client, product_factory, faker):
    product = product_factory()

    response = client.get(reverse('products:products_list'))
    assert response.status_code == 200
    assert response.template_name[0] == 'products/products_list.html'
    assert len(response.context['products']) == 5

    response = client.get(reverse('products:products_detail', args=(str(product.id),)))
    assert response.status_code == 200

    response = client.get(reverse('products:products_detail', args=(faker.uuid4(),)))
    assert response.status_code == 404


def test_export_csv(client, product_factory):
    url = reverse('products:export_csv')
    product1 = product_factory()
    product2 = product_factory()

    response = client.get(url)
    assert product1.name in str(response.content)
    assert product2.name in str(response.content)


def test_import_csv(login_user, faker):
    url = reverse('products:import_csv')

    client, user = login_user

    fieldnames = ['name', 'description', 'price', 'sku', 'category', 'image']
    tempt_file = 'tmp.csv'
    with open(tempt_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(fieldnames)
        for _ in range(0, 3):
            writer.writerow(
                [faker.pystr(min_chars=4, max_chars=10),
                 faker.pystr(min_chars=4, max_chars=10),
                 faker.pydecimal(positive=True, min_value=1,
                                 left_digits=2,
                                 right_digits=2,),
                 faker.pystr(min_chars=4, max_chars=10),
                 faker.pystr(min_chars=4, max_chars=10),
                 None]
            )
    data = open(tempt_file, 'rb')
    response = client.post(url, data={'file': data})

    assert response.status_code == 302
    assert Product.objects.count() == 3

    os.remove(tempt_file)

