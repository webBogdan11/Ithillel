from django.urls import reverse
from feedback.models import Feedback
from django.core.cache import cache


def test_feedback_view(login_user, client, faker):
    cache.clear()
    url = reverse('feedback:feedbacks')

    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('users:login') + '?next=' + url

    client, user = login_user

    response = client.get(url)

    assert response.status_code == 200
    assert b'Leave you feedback' in response.content
    assert len(Feedback.get_feedbacks()) == 0
    assert not Feedback.objects.exists()

    text = faker.text()
    data = {
        'user': str(user.id),
        'text': text,
        'rating': 3
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert Feedback.objects.exists()
    assert str(Feedback.objects.first()) == f'{text[:10]}'
    assert len(Feedback.get_feedbacks()) == 1

