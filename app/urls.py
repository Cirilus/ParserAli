from django.urls import path, include
from .views import ParseProduct, ProductsAllView, ProductFullView
from rest_framework import routers

router = routers.DefaultRouter()
router.register('products', ProductsAllView, basename="part_product")

urlpatterns = [
    path('scrape/', ParseProduct.as_view(), name="scrape_data"),
    path("", include(router.urls)),
    path('products/<int:id>/', ProductFullView.as_view({"get": "list"}), name="product"),

]
