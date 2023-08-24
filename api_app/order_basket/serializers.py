from rest_framework import serializers

from orders.models import Order
from products.models import Basket
from store.config import DOMAIN_NAME


class BasketSerializers(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    product = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Basket
        fields = ['user', 'product', 'quantity', 'create_at']


class OrderSerializers(serializers.ModelSerializer):
    initial = serializers.SlugRelatedField(slug_field='username', read_only=True)
    link_detail = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'initial', 'basket_history', 'link_detail']

    def get_link_detail(self, obj):
        return f'{DOMAIN_NAME}api/v1/order/{obj.pk}'

    def create(self, validated_data):
        user = self.context['request']
        baskets = Basket.objects.filter(user=user)
        order = Order.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            address=validated_data['address'],
            initial=user,
            basket_history={
                'purchased_items': [basket.de_json() for basket in baskets],
                'total_sum': round(float(baskets.total_sum()), 2),
            }
        )
        baskets.delete()
        return order


class OrderDetailSerializers(serializers.ModelSerializer):
    initial = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'



