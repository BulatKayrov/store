from rest_framework import serializers

from products.models import ProductCategory, Product


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        exclude = ['description']


class ProductSerializers(serializers.ModelSerializer):
    category = CategorySerializers()

    class Meta:
        model = Product
        fields = '__all__'
