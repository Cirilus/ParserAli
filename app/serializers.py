from .models import Product, Project, ProjectProduct
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


class ProjectProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectProduct
        fields = ("title", "parameters")


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "title")


class DetailProjectSerializer(serializers.ModelSerializer):
    products = ProjectProductSerializer(many=True)
    class Meta:
        model = Project
        fields = ("id", "title", "products")


