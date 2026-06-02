from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User
from api.permissions import UserPermissions
from api.serializers import (
    LoginSerializer,
    UserSerializer,
    UserUpdateSerializer,
)


class UserListCreateAPIView(generics.ListCreateAPIView):
    """POST is open registration; GET (listing all users) is admin-only."""

    queryset = User.objects.all().order_by("-created_at")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAdminUser()]


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [UserPermissions]


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
