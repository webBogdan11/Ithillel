import csv

from django.contrib import messages
from django.http import HttpResponse
from django.db.models import OuterRef, Exists
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView
from django_filters.views import FilterView
from products.models import Product
from products.forms import ContactForm
from products.tasks import send_contact_form
from products.tasks import parse_products
from products.filters import ProductFilter
from products.forms import ImportCSVForm
from favorite.models import Favorite


class IndexView(FormView):
    template_name = 'products/index.html'
    form_class = ContactForm
    success_url = reverse_lazy('products:index')

    def form_valid(self, form):
        send_contact_form.delay(email=form.cleaned_data['email'],
                                text=form.cleaned_data['text'])
        messages.success(self.request, 'Email has been send.')

        return super().form_valid(form)


class ProductsView(FilterView):
    model = Product
    context_object_name = 'products'
    paginate_by = 10
    filterset_class = ProductFilter
    template_name = 'products/products_list.html'

    def get_queryset(self):
        qs = self.model.get_products()
        if self.request.user.is_authenticated:
            sq = Favorite.objects.filter(
                product=OuterRef('id'),
                user=self.request.user
            )
            qs = qs.annotate(is_favorite=Exists(sq))

        return qs.select_related('category').prefetch_related('products')


# class ProductsListView(ListView):
#     model = Product
#     context_object_name = 'products'
#     paginate_by = 10
#     template_name = 'products/products_list.html'
#     filter_form = ProductFilterForm
#
#     def filtered_queryset(self, queryset):
#         category_id = self.request.GET.get('category')
#         currency = self.request.GET.get('currency')
#         name = self.request.GET.get('name')
#         if category_id:
#             queryset = queryset.filter(category_id=category_id)
#             self.filter_form.base_fields['category'].initial = Category.objects.get(id=category_id)
#         if currency:
#             queryset = queryset.filter(currency=currency)
#             self.filter_form.base_fields['currency'].initial = currency
#         if name:
#             queryset = queryset.filter(name__icontains=name)
#             self.filter_form.base_fields['name'].initial = name
#
#         return queryset
#
#     def get_queryset(self):
#         qs = self.model.get_products()
#         qs = self.filtered_queryset(qs)
#         return qs.select_related('category').prefetch_related('products')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(object_list=None, **kwargs)
#         context.update(
#             {'filter_form': self.filter_form}
#         )
#         return context


class ProductsDetail(DetailView):
    template_name = 'products/products_detail.html'
    model = Product
    context_object_name = 'product'

    def get_queryset(self):
        product = super().get_queryset()
        return product.prefetch_related('products')


def export_csv(request, *args, **kwargs):
    response = HttpResponse(
        content_type='text/csv',
        headers={
             'Content-Disposition': 'attachment; filename="products.csv"'
        }
    )
    fieldnames = ['name', 'description', 'price', 'sku', 'category', 'image']
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    for product in Product.objects.iterator():
        writer.writerow(
            {
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'sku': product.sku,
                'category': product.category,
                'image': None,
            }
        )
    return response


class ImportCSV(FormView):
    form_class = ImportCSVForm
    template_name = 'products/products_csv_import.html'
    success_url = reverse_lazy('products:index')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


def parse_products_view(request):
    parse_products.delay()
    return HttpResponse('Hello')
