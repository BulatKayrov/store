from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from .serializers import BasketSerializers, OrderSerializers, OrderDetailSerializers
from products.models import Basket
from ..custom_pagination import CustomPagination


class BasketListAPIVIew(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BasketSerializers
    queryset = Basket.objects.all()

    def get_queryset(self):
        qs = self.queryset.filter(user=self.request.user)
        return qs


class OrderListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.queryset.filter(initial=self.request.user)


class OrderCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializers

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request.user
        return context


class OrderDetailAPIView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializers
