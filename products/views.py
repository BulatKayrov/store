from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views import generic

from .models import Basket, Product, ProductCategory


class IndexView(generic.TemplateView):
    """Вью отображение стартовой страницы"""
    template_name = 'products/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['title'] = 'Store'
        return context


class ProductsListView(generic.ListView):
    model = Product
    template_name = 'products/products.html'
    context_object_name = 'products'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            return queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Store - каталог'
        context['categories'] = ProductCategory.objects.all()
        return context


# def products(request, pk=None, page=1):
#
#     """Вью отображение страницы с продуктами"""
#
#     if pk:
#         product = Product.objects.filter(category_id=pk)
#     else:
#         product = Product.objects.all()
#
#     paginator = Paginator(object_list=product, per_page=3)
#     products_paginator = paginator.page(page)
#
#     context = {
#         'title': 'Store',
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator,
#     }
#
#     return render(request, 'products/products.html', context=context)


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
