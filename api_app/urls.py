from django.urls import path

from .views import CategoryListAPIView, ProductListAPIView

app_name = 'api_app'

urlpatterns = [
    path('category/', CategoryListAPIView.as_view(), name='category_api'),
    path('product/', ProductListAPIView.as_view(), name='product_api'),
]
