from django.urls import reverse


def test_feedback_view(client):
    response = client.get(reverse('feedback:feedbacks'), follow=True)

    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('users:login') + '?next=' + reverse('feedback:feedbacks')
