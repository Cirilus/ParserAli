from urllib.parse import urlparse
from uuid import uuid4
from django.http import JsonResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from scrapyd_api import ScrapydAPI
from rest_framework import serializers

from .serializers import ProductFullSerializer, ProductBaseSerializer, ParseSerializer
from .models import Product

scrapyd = ScrapydAPI('http://localhost:6800')


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return False
    return True


@extend_schema(tags=["product"], operation_id="allProducts",
               summary="return name and iamges of all products that ralated to user")
class ProductsAllView(GenericViewSet, ListModelMixin):
    serializer_class = ProductBaseSerializer
    queryset = Product.objects.all()


@extend_schema(tags=["product"], operation_id="fullProduct", summary="return all info about product by id")
class ProductFullView(GenericViewSet, ListModelMixin):
    serializer_class = ProductFullSerializer

    def get_queryset(self):
        id = self.kwargs['id']
        try:
            return Product.objects.filter(pk=id)
        except Product.DoesNotExist:
            return Product.objects.last()


class ParseProduct(APIView):
    @extend_schema(tags=["scrape"],
                   parameters=[OpenApiParameter(name='url', type=OpenApiTypes.STR, location=OpenApiParameter.PATH)],
                   responses=ParseSerializer,
                   summary="run a parser requirement url")
    def post(self, request):
        url = request.data['url']
        if not url:
            return JsonResponse({"error": "Missing url"})

        if not is_valid_url(url):
            return JsonResponse({'error': "Url is invalid"})

        domain = urlparse(url).netloc
        unique_id = str(uuid4())

        if domain != "aliexpress.ru" and domain != "m.aliexpress.ru":
            return JsonResponse({'error': "Domain is invalid"})

        settings = {
            'unique_id': unique_id,
            'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }

        task = scrapyd.schedule('default', 'Ali',
                                settings=settings,
                                url=url, domain=domain)
        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started'})
