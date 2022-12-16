from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core import mail
import re


User = get_user_model()


def test_login_user(client, faker):
    email = faker.email()
    password = faker.password()
    phone = faker.phone_number()
    url = reverse('users:login')
    user = User.objects.create(
        email=email,
        first_name=email,
        phone=phone,
        is_phone_valid=True
    )
    user.set_password(password)
    user.save()
    # get login page
    response = client.get(url)

    assert response.status_code == 200

    data = {
        'password': faker.password()
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'][0] == 'Email or phone number is required.'

    data['username'] = faker.email()
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'][0] == 'Please enter a correct email address and password. ' \
                                                            'Note that both fields may be case-sensitive.'

    del data['username']
    data['phone'] = faker.word()
    data['password'] = password
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'][0] == 'Please enter a correct email address and password. ' \
                                                            'Note that both fields may be case-sensitive.'

    data['username'] = email
    data['password'] = password
    response = client.post(url, data=data)
    assert response.status_code == 302

    del data['username']
    data['phone'] = phone
    response = client.post(url, data=data)
    assert response.status_code == 302


def test_register_user(client, faker):
    email = faker.email()
    password = faker.password()

    url = reverse('users:register')

    assert not User.objects.filter(email=email).exists()
    assert len(mail.outbox) == 0

    data = {
        'password1': password,
        'password2': password,
        'email': email,
    }
    response = client.post(url, data=data)
    assert response.status_code == 302
    assert User.objects.filter(email=email, is_active=False).exists()
    assert len(mail.outbox) == 1

    response = client.post(reverse('users:login'),
                           data={'email': email, 'password': password})
    assert response.status_code == 200

    uidb64, token = re.search("registration/(.*)/(.*)/confirm",
                              mail.outbox[0].body).groups()

    response = client.get(reverse('users:registration_confirm',
                                  args=(uidb64, token)))
    assert response.status_code == 302
    assert User.objects.filter(email=email, is_active=True).exists()

    response = client.post(reverse('users:login'),
                           data={'username': email, 'password': password})
    assert response.status_code == 302

