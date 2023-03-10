from django.urls import path, include
from .views import ParseProduct, ProductsView, ProductDetailView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('products', ProductsView, basename="products")
# router.register(f'products/{id}/', ProductDetailView, basename="product_detail")

urlpatterns = [
    path('scrape/', ParseProduct.as_view(), name="scrape_data"),
    path("", include(router.urls)),
    path('products/<int:id>/', ProductDetailView.as_view({"get": "retrieve", "DELETE": "destroy"}), name="product"),

]
