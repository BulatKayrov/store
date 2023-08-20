from rest_framework import generics

from .serializers import CategorySerializers, ProductSerializers
from products.models import ProductCategory, Product


class CategoryListAPIView(generics.ListAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializers


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers

