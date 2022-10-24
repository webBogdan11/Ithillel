import decimal

from django.shortcuts import render, redirect
import csv
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView
from products.models import Product, Category

from products.forms import CsvImport


class IndexView(TemplateView):
    template_name = 'products/index.html'


class ProductsListView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/products_list.html'


class ProductsDetail(DetailView):
    template_name = 'products/products_detail.html'
    model = Product
    context_object_name = 'product'


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


def import_csv(request):
    form = CsvImport()
    if request.method == "POST":
        form = CsvImport(data=request.POST, files=request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file'].read()
            file_str = file.decode('utf-8').strip().split('\n')
            file_csv = csv.reader(file_str, delimiter=',')
            next(file_csv)
            for row in file_csv:
                Product.objects.create(name=row[0],
                                       description=row[1],
                                       price=decimal.Decimal(row[2]),
                                       sku=row[3],
                                       category=Category.objects.get(name=row[4]))
            return redirect(reverse_lazy('products:products_list'))

    return render(request,
                  'products/products_csv_import.html',
                  {'form': form})
