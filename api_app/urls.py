from django.urls import path

from .views import (
    CategoryListAPIView, ProductListAPIView, CategoryRUDAPIView, ProductChangeAPIView,
    BasketListCreateAPIView, OrderListCreateApiView
)

app_name = 'api_app'

urlpatterns = [
    path('category/', CategoryListAPIView.as_view(), name='categories_api'),
    path('category/<int:pk>/', CategoryRUDAPIView.as_view(), name='category_api'),
    path('product/', ProductListAPIView.as_view(), name='product_api'),
    path('crud/product/', ProductChangeAPIView.as_view(), name='create_product_api'),

    path('add/basket/', BasketListCreateAPIView.as_view(), name='add_basket_api'),
    path('orders/', OrderListCreateApiView.as_view(), name='order_api'),
]
