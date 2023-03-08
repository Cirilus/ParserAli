from drf_spectacular.utils import extend_schema
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer
from .models import CustomUser

@extend_schema(summary="Return the info about register user")
class UserView(GenericViewSet, ListModelMixin):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):

        return [self.request.user]
