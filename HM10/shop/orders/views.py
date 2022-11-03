from django.shortcuts import render # noqa
from django.views.generic import RedirectView, TemplateView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.urls import reverse_lazy

from orders.mixins import GetCurrentOrderMixin
from orders.tasks import send_to_console_task
from orders.forms import UpdateCartOrderForm, RecalculateCartForm


class CartView(GetCurrentOrderMixin, TemplateView):
    template_name = 'orders/cart.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {'order': self.get_object(),
             'products_relation': self.get_queryset()}
        )
        return context

    def get_queryset(self):
        print(self.get_object().products.through.objects)
        return self.get_object().products.through.objects\
            .filter(order=self.get_object()) \
            .select_related('product') \
            .annotate(full_price=F('product__price') * F('quantity'))


class UpdateCartView(GetCurrentOrderMixin, RedirectView):

    def post(self, request, *args, **kwargs):
        form = UpdateCartOrderForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save(kwargs.get('action'))
        return self.get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy(
            'orders:cart' if kwargs['action'] == 'remove' else 'products:products_list')


class RecalculateCartView(GetCurrentOrderMixin, RedirectView):
    url = reverse_lazy('orders:cart')

    def post(self, request, *args, **kwargs):
        form = RecalculateCartForm(request.POST, instance=self.get_object())
        if form.is_valid():
            form.save()
        return self.get(request, *args, **kwargs)


class PurchaseView(GetCurrentOrderMixin, View):
    template_name = 'orders/cart_purchase.html'

    def post(self, request):
        self.get_object().pay()
        send_to_console_task.delay()
        return render(request, self.template_name)
