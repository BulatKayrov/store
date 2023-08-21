from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Order
from .custom_permissions import IsReadAllCreateAdmin, IsRetrieveDestroyUpdateDefinedUsers
from .serializers import CategorySerializers, ProductSerializers, BasketSerializers, OrderSerializers
from products.models import ProductCategory, Product, Basket


class OrderListCreateApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Order.objects.filter(initial=request.user)
        serializers = OrderSerializers(data=queryset, many=True)
        serializers.is_valid(raise_exception=True)
        return Response({'result': serializers.data})

    def post(self, request):
        basket_qs = Basket.objects.filter(user=request.user)
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']
        address = request.data['address']
        Order.objects.create(
            initial=request.user, first_name=first_name, last_name=last_name, email=email,
            address=address, basket_history={
                'purchased_items': [basket.de_json() for basket in basket_qs],
                'total_sum': round(float(basket_qs.total_sum()), 2),
            }
        )
        return Response({})


class BasketListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Basket.objects.filter(user=request.user)
        serializers = BasketSerializers(data=queryset, many=True)
        serializers.is_valid(raise_exception=True)
        return Response({'result': serializers.data})

    def post(self, request):
        product = Product.objects.get(id=request.data['product'])
        queryset = Basket.objects.filter(user=request.user, product=product)
        if queryset.exists():
            basket = queryset.first()
            basket.quantity += request.data['quantity']
            basket.save()
            return Response(status=200)
        else:
            Basket.objects.create(user=request.user, product_id=request.data['product'],
                                  quantity=request.data['quantity'])
            return Response(status=200)


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
