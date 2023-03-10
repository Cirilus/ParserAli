from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserView, CreateUserView, UpdateUserView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('me/', UserView.as_view({"get":"retrieve"}), name="user_info"),
    path('signUp/', CreateUserView.as_view(), name="user_create"),
    path('update/', UpdateUserView.as_view(), name="user_update")
]
