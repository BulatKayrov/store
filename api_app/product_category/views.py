
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser

from api_app.custom_pagination import CustomPagination
from api_app.custom_permissions import IsReadAllCreateAdmin, IsRetrieveDestroyUpdateDefinedUsers
from api_app.product_category.serializers import CategorySerializers, ProductSerializers
from products.models import ProductCategory, Product


class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsReadAllCreateAdmin]


class CategoryRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsRetrieveDestroyUpdateDefinedUsers]


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['name']
    filterset_fields = [
        'category__name'
    ]
    ordering_fields = ['price', 'quantity']
    pagination_class = CustomPagination


class ProductChangeAPIView(mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)