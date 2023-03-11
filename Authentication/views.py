from drf_spectacular.utils import extend_schema
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework import permissions

from django.contrib.auth import get_user_model
from .serializers import UserSerializer, CreateUserSerializer, UpdateUserSerializer

from .models import CustomUser


@extend_schema(summary="Return the info about user that logged in")
class UserView(GenericViewSet, RetrieveModelMixin):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user


@extend_schema(summary="Register an user")
class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CreateUserSerializer


@extend_schema(summary="Update an info about existing user")
class UpdateUserView(UpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UpdateUserSerializer
    http_method_names = ['patch']

    def get_object(self):
        return self.request.user




