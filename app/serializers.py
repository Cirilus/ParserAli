from .models import Product
from rest_framework import serializers


class ProductSerializer(Product):
    class Meta:
        model = Product
        fields = ["__all__"]