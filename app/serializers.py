from .models import Product, Project, ProjectProduct
from rest_framework import serializers


class ProductFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('unique_id', 'name', 'images','from_whom', "prices", 'parameters', 'additional_parameters',)
        extra_kwargs = {
            'unique_id': {'read_only': True},
            'images': {'read_only': True},
            'additional_parameters': {'read_only': True},
            'prices': {'read_only': True},
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
    full_price = serializers.SerializerMethodField(read_only=True)

    def get_full_price(self, instance):
        return instance.price * instance.count

    class Meta:
        model = ProjectProduct
        fields = ("id", "title", "parameters", "from_whom", "count", "project", "price", "full_price")
        extra_kwargs = {
            'id': {'read_only':True},
            'project': {'write_only': True},
        }


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("id", "title", "user")
        extra_kwargs = {
            'id': {'read_only': True},
        }


class DetailProjectSerializer(serializers.ModelSerializer):
    products = ProjectProductSerializer(many=True)
    class Meta:
        model = Project
        fields = ("id", "title", "products",)

