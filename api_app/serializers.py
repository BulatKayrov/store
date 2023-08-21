from rest_framework import serializers

from orders.models import Order
from products.models import ProductCategory, Product, Basket


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        exclude = ['description']


class ProductSerializers(serializers.ModelSerializer):
    category = CategorySerializers()

    class Meta:
        model = Product
        fields = '__all__'


class BasketSerializers(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = ['product', 'quantity']


class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

