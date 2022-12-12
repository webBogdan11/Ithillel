from django.contrib.auth import get_user_model
from django.urls import reverse

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


def test_register_user(client, faker, user_usual):
    url = reverse('users:register')

    response = client.get(url)
    assert response.status_code == 200
    assert response.template_name[0] == 'users/register.html'

    email = faker.email()

    data = {
        'email': email
    }

    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors == {'password1': ['This field is required.'],
                                               'password2': ['This field is required.']}

    data['password1'] = faker.password()
    data['password2'] = faker.password()

    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors == {'password2': ['The two password fields didn’t match.']}

    data['password2'] = data['password1']

    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('products:index')

    data['email'] = user_usual.email
    response = client.post(url, data=data)

    assert response.status_code == 200
    assert response.context['form'].errors['__all__'] == ['A user with that username already exists.']

