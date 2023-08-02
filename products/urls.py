from django.urls import path
from .views import IndexView, ProductsListView, basket_add, basket_remove

app_name = 'products'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('products/', ProductsListView.as_view(), name='products'),
    path('products/<int:category_id>/', ProductsListView.as_view(), name='products'),
    path('page/<int:page>/', ProductsListView.as_view(), name='paginator'),
    path('basket/add/<int:pk>/', basket_add, name='baskets'),
    path('basket/remove/<int:pk>/', basket_remove, name='basket_remove'),
]
