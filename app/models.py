from django.db import models
from jsonfield import JSONField
from Authentication.models import CustomUser


class Product(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    name = models.TextField()
    images = JSONField()
    parameters = JSONField()
    prices = models.TextField()
    additional_parameters = models.TextField()
    from_whom = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products", null=True, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.TextField(blank=False, null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.title


class ProjectProduct(models.Model):
    title = models.TextField(blank=False, null=False)
    parameters = JSONField()
    from_whom = models.TextField()
    price = models.IntegerField()
    count = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.title


