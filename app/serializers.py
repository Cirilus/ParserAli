from .models import Product, Project, ProjectProduct
from rest_framework import serializers


class ProductFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('unique_id', 'name', 'images', 'parameters', 'additional_parameters', 'from_whom')
        extra_kwargs = {
            'unique_id': {'read_only': True},
            'images': {'read_only': True},
            'additional_parameters': {'read_only': True},
        }


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
        fields = ("title", "parameters", "from_whom", "count", "project")
        extra_kwargs = {
            'project': {'write_only': True},
        }


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "title", "user")
        extra_kwargs = {
            'id': {'read_only': True},
            'user': {'write_only': True},
        }


class DetailProjectSerializer(serializers.ModelSerializer):
    products = ProjectProductSerializer(many=True)
    class Meta:
        model = Project
        fields = ("id", "title", "products",)

