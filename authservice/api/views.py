from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User
from api.permissions import UserPermissions
from api.serializers import (
    LoginSerializer,
    UserSerializer,
    UserUpdateSerializer,
)


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [UserPermissions]


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
