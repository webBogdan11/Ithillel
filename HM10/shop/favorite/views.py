from django.views.generic import RedirectView, ListView
from favorite.forms import UpdateFavoriteForm
from django.urls import reverse_lazy
import json
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.decorators import ajax_required
from django.views import View
from django.http import JsonResponse
from favorite.models import Favorite
from products.models import Product


class FavoriteView(ListView):
    template_name = 'favorite/favorite_list.html'
    model = Favorite
    context_object_name = 'favorites'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        favorites = super().get_queryset()
        return favorites.filter(user=self.request.user).select_related('product')


class UpdateFavoriteView(RedirectView):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = UpdateFavoriteForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(kwargs.get('action'))
        else:
            messages.error(self.request,
                           f'Wrong product id')

        return self.get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy(
            'favorite:favorite_list' if kwargs['action'] == 'remove' else 'products:products_list')


class AJAXFavoriteProductAddOrRemoveView(View):

    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = json.load(request).get('data')
        form = UpdateFavoriteForm(data, user=request.user)
        if form.is_valid():
            form.save()
        else:
            return JsonResponse(data={'error': form.errors}, status=400)

        return JsonResponse(data={'success': True,
                                  'action': data['action']})
