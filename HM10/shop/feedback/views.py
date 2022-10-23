from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from feedback.models_form import FeedbackModelForm
from feedback.models import Feedback


@login_required
def feedback(request):
    user = request.user
    if request.method == 'POST':
        form = FeedbackModelForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
    else:
        form = FeedbackModelForm(user=user)
    context = {
        'feedbacks': Feedback.objects.all(),
        'form': form
    }
    return render(request, 'feedback/feedback.html', context)
