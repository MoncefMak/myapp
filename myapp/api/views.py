from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView  # new

from accounts.models import User
from api.permissions import UserPermissions
from api.serializer.serializers_user import UserSerializer, UserUpdateSerializer, LogInSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [UserPermissions]


class LogInView(TokenObtainPairView):  # new
    serializer_class = LogInSerializer
