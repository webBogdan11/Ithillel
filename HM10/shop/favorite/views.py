from django.views.generic import RedirectView, TemplateView
from favorite.forms import UpdateFavoriteForm
from django.urls import reverse_lazy


class FavoriteView(TemplateView):
    template_name = 'favorite/favorite_list.html'


class UpdateFavoriteView(RedirectView):

    def post(self, request, *args, **kwargs):
        form = UpdateFavoriteForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(kwargs.get('action'))
        return self.get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy(
            'favorite:favorite_list' if kwargs['action'] == 'remove' else 'products:products_list')
