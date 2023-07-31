from django.urls import path

from .views import IndexView, products, basket_add, basket_remove

app_name = 'products'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/', products, name='products'),
    path('products/<int:pk>/', products, name='products'),
    path('page/<int:page>/', products, name='paginator'),
    path('baskeet/add/<int:pk>/', basket_add, name='baskets'),
    path('baskeet/remove/<int:pk>/', basket_remove, name='basket_remove'),
]
