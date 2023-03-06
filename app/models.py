from django.db import models

from Authentication.models import CustomUser


class Product(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    name = models.TextField()
    images = models.TextField()
    parameters = models.TextField()
    additional_parameters = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products", null=True, blank=True)

    def __str__(self):
        return self.name
