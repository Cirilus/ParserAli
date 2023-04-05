import json
from urllib.parse import urlparse
from uuid import uuid4
from django.http import JsonResponse, HttpResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import DestroyModelMixin, \
    ListModelMixin, RetrieveModelMixin, \
    UpdateModelMixin, CreateModelMixin
from rest_framework.generics import CreateAPIView
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from rest_pandas import PandasSimpleView
from scrapyd_api import ScrapydAPI
from django.shortcuts import get_object_or_404

from .serializers import ProductFullSerializer, \
    ProductBaseSerializer, ParseSerializer, \
    ProjectSerializer, DetailProjectSerializer, \
    ProjectProductSerializer
from .models import Product, Project, ProjectProduct
from rest_framework import permissions
import pandas as pd


scrapyd = ScrapydAPI('http://localhost:6800')


def is_valid_url(url):
    validate = URLValidator()
    try:
        validate(url)
    except ValidationError:
        return False
    return True


class ProductPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limits'
    max_page_size = 100


@extend_schema(tags=["product"],
               summary="return name and iamges of all products that ralated to user")
class ProductsView(GenericViewSet, ListModelMixin):
    serializer_class = ProductBaseSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        products = Product.objects.filter(user=self.request.user)
        return products


@extend_schema_view(
    retrieve=extend_schema(
        tags=['product'],
        summary="return all info about product by id",
    ),
    destroy=extend_schema(
        tags=['product'],
        summary="delete the product",
    ),
    partial_update=extend_schema(
        tags=['product'],
        summary="update the product"
    )
)
class DetailProductView(GenericViewSet,
                        RetrieveModelMixin,
                        DestroyModelMixin,
                        UpdateModelMixin):
    serializer_class = ProductFullSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["patch", "get", "delete"]

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(Product, pk=pk)


@extend_schema_view(
    list=extend_schema(
        tags=['project'],
        summary="return id and title of all projects that related to user",
    ),
    create=extend_schema(
        tags=['project'],
        summary="create the project",
    ),
)
class ProjectView(GenericViewSet,
                  ListModelMixin,
                  CreateModelMixin):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        projects = Project.objects.filter(user=self.request.user)
        return projects

    def create(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        return super().create(request, *args, **kwargs)


@extend_schema_view(
    retrieve=extend_schema(
        tags=['project'],
        summary="return all products of current project",
    ),
    destroy=extend_schema(
        tags=['project'],
        summary="delete the project",
    ),
)
class DetailProjectView(GenericViewSet,
                        RetrieveModelMixin,
                        DestroyModelMixin):
    serializer_class = DetailProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(Project, pk=pk)


@extend_schema_view(
    create=extend_schema(
        tags=['project'],
        summary="Create the product of project",
    ),
    destroy=extend_schema(
        tags=['project'],
        summary="delete the product from project",
    ),
    partial_update=extend_schema(
        tags=['project'],
        summary="Update the product of project"
    )

)
class ProjectProductView(GenericViewSet,
                     CreateModelMixin,
                     DestroyModelMixin,
                     UpdateModelMixin):
    serializer_class = ProjectProductSerializer
    queryset = ProjectProduct
    http_method_names = ["patch", "post", "delete"]
    permission_classes = [permissions.IsAuthenticated]


class SendCsvView(APIView):
    serializer_class = ProjectProductSerializer
    def get(self, request):
        products = ProjectProduct.objects.all()
        products = self.serializer_class(products, many=True).data
        df = pd.DataFrame(products)
        csv = df.to_csv()
        response = HttpResponse(csv, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'


        return response


class ParseProduct(APIView):
    permission_classes = [permissions.IsAuthenticated]
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
                                url=url, domain=domain,
                                kwargs=self.request.user.pk)

        return JsonResponse({'task_id': task, 'unique_id': unique_id, 'status': 'started'})
