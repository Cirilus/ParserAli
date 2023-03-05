from urllib.parse import urlparse
from uuid import uuid4

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from scrapyd_api import ScrapydAPI
from drf_yasg.utils import swagger_auto_schema

from .serializers import ProductSerializer, PartProductSerializer
from .models import Product


scrapyd = ScrapydAPI('http://localhost:6800')


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return False
    return True

@method_decorator(name="list", decorator=swagger_auto_schema(operation_summary="return info about all products"))
class PartProductsView(GenericViewSet, ListModelMixin):
    serializer_class = PartProductSerializer
    queryset = Product.objects.all()

@method_decorator(name="list", decorator=swagger_auto_schema(operation_summary="return the full product's info by id "))
class ProductsView(GenericViewSet, ListModelMixin):
    serializer_class = ProductSerializer
    def get_queryset(self):
        id = self.kwargs['id']
        try:
            return Product.objects.filter(pk=id)
        except Product.DoesNotExist:
            return Product.objects.last()

class ParseProduct(APIView):
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
