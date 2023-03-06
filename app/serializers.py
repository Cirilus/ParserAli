from .models import Product
from rest_framework import serializers


class ProductFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'images']

class ParseSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    unique_id = serializers.CharField()
    status = serializers.CharField()