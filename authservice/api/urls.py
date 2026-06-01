from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, UserCreateAPIView, UserRetrieveUpdateAPIView

urlpatterns = [
    path('users/', UserCreateAPIView.as_view(), name='user-create'),
    path('users/<uuid:pk>/', UserRetrieveUpdateAPIView.as_view(), name='user-update'),
    path('login/', LoginView.as_view(), name='log_in'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
