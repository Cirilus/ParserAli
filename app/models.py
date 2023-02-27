from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    name = models.TextField()
    images = models.TextField()
    parameters = models.TextField()
    additional_parameters = models.TextField()

    def __str__(self):
        return self.name
