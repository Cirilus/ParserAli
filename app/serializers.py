from .models import Product
from rest_framework import serializers


class ProductFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('unique_id', 'name', 'images', 'parameters', 'additional_parameters', 'from_whom')


class ProductBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'images']


class ParseSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    unique_id = serializers.CharField()
    status = serializers.CharField()
