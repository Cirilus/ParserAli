from django.db import models

from Authentication.models import CustomUser


class Product(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    name = models.TextField()
    images = models.TextField()
    parameters = models.TextField()
    additional_parameters = models.TextField()
    from_whom = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="products", null=True, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.title


class ProjectProduct(models.Model):
    title = models.TextField()
    parameters = models.TextField()
    from_whom = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="products")

    def __str__(self):
        return self.title


