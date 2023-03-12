from django.urls import path, include
from .views import ParseProduct, ProductsView, \
    DetailProductView, ProjectView, DetailProjectView\
    , ProjectProduct
from rest_framework import routers

router = routers.DefaultRouter()
router.register('products', ProductsView, basename="products")
router.register(r'products', DetailProductView, basename="product")
router.register(r'projects', ProjectView, basename="projects")
router.register(r'projects', DetailProjectView, basename="project")
router.register(r'product_project', ProjectProduct, basename="create_project_product")


urlpatterns = [
    path('scrape/', ParseProduct.as_view(), name="scrape_data"),
    path("", include(router.urls)),
]
