from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView  # new

from .views import UserCreateAPIView, RetrieveUpdateAPIView, LogInView

urlpatterns = [
    path('users/', UserCreateAPIView.as_view(), name='user-create'),
    path('users/<uuid:pk>/', RetrieveUpdateAPIView.as_view(), name='user-update'),
    path('login/', LogInView.as_view(), name='log_in'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
