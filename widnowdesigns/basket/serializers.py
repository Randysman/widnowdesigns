from main.models import Product
from rest_framework import serializers
from decimal import Decimal
from main.serializers import ProductSerializer


class BasketAddProductSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1, default=1)
    override = serializers.BooleanField(default=False, required=False)


class BasketItemSerializer(serializers.Serializer):
    product = ProductSerializer()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_price = serializers.SerializerMethodField
    discounted_price = serializers.SerializerMethodField

