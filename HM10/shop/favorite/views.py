from django.views.generic import RedirectView, ListView
from favorite.forms import UpdateFavoriteForm
from django.urls import reverse_lazy
from favorite.models import Favorite


class FavoriteView(ListView):
    template_name = 'favorite/favorite_list.html'
    model = Favorite
    context_object_name = 'favorites'

    def get_queryset(self):
        favorites = super().get_queryset()
        return favorites.filter(user=self.request.user).select_related('product')


class UpdateFavoriteView(RedirectView):

    def post(self, request, *args, **kwargs):
        form = UpdateFavoriteForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(kwargs.get('action'))
        return self.get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy(
            'favorite:favorite_list' if kwargs['action'] == 'remove' else 'products:products_list')
