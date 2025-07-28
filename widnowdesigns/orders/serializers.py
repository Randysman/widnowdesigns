from main.models import Product
from .models import Order, OrderItem
from rest_framework import serializers
from users.models import User


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = ['product', 'price', 'quantity']
        read_only_fields = ['price']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = [
            'user', 'first_name', 'last_name', 'email',
            'address', 'postal_code', 'city', 'paid',
            'stripe_id', 'items'
        ]
        read_only_fields = ['paid', 'stripe_id']