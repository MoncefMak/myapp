# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from myapp.accounts.models import User


class UserAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client = APIClient()

    def get_access_token(self):
        refresh = RefreshToken.for_user(self.user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def test_create_user(self):
        url = '/api/users/'
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpassword'}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_patch_user(self):
        url = f'/api/users/{self.user.id}/'
        data = {'username': 'updateduser'}

        access_token = self.get_access_token()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_user(self):
        url = f'/api/users/{self.user.id}/'
        data = {'username': 'updateduser', 'email': 'updatenewuser@example.com'}

        access_token = self.get_access_token()['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_user(self):
        url = '/api/login/'
        data = {
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data, format='json')
        if response.status_code == status.HTTP_200_OK:
            self.assertIn('access', response.data)
            self.assertIn('refresh', response.data)
        elif response.status_code == status.HTTP_400_BAD_REQUEST:
            print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token(self):
        refresh_url = '/api/login/refresh/'
        access_token = self.get_access_token()['refresh']

        refresh_data = {'refresh': access_token}
        response = self.client.post(refresh_url, refresh_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('access', response.data)
