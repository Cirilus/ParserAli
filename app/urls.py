from django.urls import path
from .views import ParseProduct, PartProductsView, ProductsView

urlpatterns = [
    path('scrape/', ParseProduct.as_view(), name="scrape_data"),
    path('products/', PartProductsView.as_view({'get': 'list'}), name="part_product"),
    path('products/<int:id>/', ProductsView.as_view({'get': 'list'}), name="product"),
]
