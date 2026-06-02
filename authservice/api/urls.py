from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import LoginView, UserListCreateAPIView, UserRetrieveUpdateAPIView

urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', UserRetrieveUpdateAPIView.as_view(), name='user-update'),
    path('login/', LoginView.as_view(), name='log_in'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
