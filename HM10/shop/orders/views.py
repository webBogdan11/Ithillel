from django.shortcuts import render # noqa
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from orders.models import Order, Discount
from products.models import Product
from orders.forms import DiscountApply


class OrderForm(TemplateView):
    template_name = "orders/orders_form.html"


@login_required
def order_add_product(request, pk):
    product = Product.objects.get(id=pk)
    order, _ = Order.objects.get_or_create(
        user=request.user,
        is_active=True
    )
    order.products.add(product)

    order.save()

    return HttpResponseRedirect(reverse_lazy("products:products_list"))


@login_required
def order_apply_discount(request):
    form = DiscountApply(data=request.POST)

    if form.errors:
        message = form.errors.as_data()["code"][0].message
    else:
        discount = form.cleaned_data['code']
        order = request.user.order.filter(is_active=True)[0]
        order.discount = discount
        order.save()
        message = 'Discount was successfully applied'

    return render(request, 'orders/orders_form.html', context={
        'message': message,
    })


def order_make_payment(request):
    order = request.user.order.filter(is_active=True)[0]
    order.is_active = False
    order.is_paid = True
    order.save()
    return render(request, 'orders/orders_payment.html')
