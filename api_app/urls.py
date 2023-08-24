from django.urls import path

from .product_category.views import CategoryListAPIView, ProductListAPIView, CategoryRUDAPIView, ProductChangeAPIView
from .order_basket.views import BasketListAPIVIew, OrderListAPIView, OrderCreateAPIView, OrderDetailAPIView
from .auth_session_app.views import UserLoginAPIView, UserLogoutAPIView

app_name = 'api_app'

urlpatterns = [
    path('session/login/', UserLoginAPIView.as_view(), name='login_api'),
    path('session/logout/', UserLogoutAPIView.as_view(), name='logout_api'),

    path('category/', CategoryListAPIView.as_view(), name='categories_api'),
    path('category/<int:pk>/', CategoryRUDAPIView.as_view(), name='category_api'),
    path('product/', ProductListAPIView.as_view(), name='product_api'),
    path('crud/product/', ProductChangeAPIView.as_view(), name='create_product_api'),

    path('basket/', BasketListAPIVIew.as_view(), name='basket_api'),
    path('orders/', OrderListAPIView.as_view(), name='orders_api'),
    path('order/create/', OrderCreateAPIView.as_view(), name='order_create_api'),
    path('order/<int:pk>/', OrderDetailAPIView.as_view(), name='order_detail_api'),

]
