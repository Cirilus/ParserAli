from django.urls import path
from .views import ParseProduct

urlpatterns = [
    path('scrape/', ParseProduct.as_view(), name="scrape_data"),
]
