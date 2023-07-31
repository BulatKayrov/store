from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic
from .models import Product, ProductCategory, Basket


class IndexView(generic.TemplateView):
    """Вью отображение стартовой страницы"""
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Store'
        return context


def products(request, pk=None, page=1):

    """Вью отображение страницы с продуктами"""

    if pk:
        product = Product.objects.filter(category_id=pk)
    else:
        product = Product.objects.all()

    paginator = Paginator(object_list=product, per_page=3)
    products_paginator = paginator.page(page)

    context = {
        'title': 'Store',
        'categories': ProductCategory.objects.all(),
        'products': products_paginator,
    }

    return render(request, 'products/products.html', context=context)


@login_required
def basket_add(request, pk):
    product = Product.objects.get(pk=pk)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, pk):
    Basket.objects.get(pk=pk).delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


