from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from django.test import TestCase

from accounts.models import User

PASSWORD = "Str0ngPass!42"


class UserAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password=PASSWORD
        )
        self.other_user = User.objects.create_user(
            username="other", email="other@example.com", password=PASSWORD
        )
        self.client = APIClient()

    def authenticate(self, user=None):
        token = RefreshToken.for_user(user or self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    # --- create / registration -------------------------------------------------
    def test_create_user_persists_and_hashes_password(self):
        url = reverse("user-create")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": PASSWORD,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.data)
        self.assertNotIn("password", response.data)  # write_only

        created = User.objects.get(email="newuser@example.com")
        self.assertNotEqual(created.password, PASSWORD)  # stored hashed
        self.assertTrue(created.check_password(PASSWORD))

    def test_create_user_rejects_weak_password(self):
        url = reverse("user-create")
        data = {"username": "weak", "email": "weak@example.com", "password": "123"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)
        self.assertFalse(User.objects.filter(email="weak@example.com").exists())

    def test_create_user_rejects_duplicate_email(self):
        url = reverse("user-create")
        data = {"username": "dup", "email": "test@example.com", "password": PASSWORD}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_rejects_duplicate_username(self):
        url = reverse("user-create")
        data = {"username": "testuser", "email": "fresh@example.com", "password": PASSWORD}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # --- retrieve --------------------------------------------------------------
    def test_retrieve_own_user(self):
        self.authenticate()
        url = reverse("user-update", args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["email"], "test@example.com")

    # --- update ----------------------------------------------------------------
    def test_patch_user_updates_username_only(self):
        self.authenticate()
        url = reverse("user-update", args=[self.user.id])
        response = self.client.patch(url, {"username": "updateduser"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        updated = User.objects.get(pk=self.user.id)
        self.assertEqual(updated.username, "updateduser")
        self.assertEqual(updated.email, "test@example.com")  # untouched by PATCH

    def test_put_user_replaces_fields(self):
        self.authenticate()
        url = reverse("user-update", args=[self.user.id])
        data = {"username": "putuser", "email": "putuser@example.com"}
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        updated = User.objects.get(pk=self.user.id)
        self.assertEqual(updated.username, "putuser")
        self.assertEqual(updated.email, "putuser@example.com")

    # --- authorization (UserPermissions) --------------------------------------
    def test_cannot_update_another_user(self):
        self.authenticate(self.user)
        url = reverse("user-update", args=[self.other_user.id])
        response = self.client.patch(url, {"username": "hacked"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.other_user.refresh_from_db()
        self.assertEqual(self.other_user.username, "other")

    def test_anonymous_cannot_update(self):
        url = reverse("user-update", args=[self.user.id])
        response = self.client.patch(url, {"username": "anon"}, format="json")
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    # --- login / JWT -----------------------------------------------------------
    def test_login_returns_tokens_and_custom_claims(self):
        url = reverse("log_in")
        response = self.client.post(
            url, {"email": "test@example.com", "password": PASSWORD}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK, msg=response.data)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        token = AccessToken(response.data["access"])
        self.assertEqual(token["username"], "testuser")
        self.assertEqual(token["email"], "test@example.com")
        self.assertEqual(token["id"], str(self.user.id))

    def test_login_wrong_password_rejected(self):
        url = reverse("log_in")
        response = self.client.post(
            url, {"email": "test@example.com", "password": "wrong-pass-99"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_unknown_email_rejected(self):
        url = reverse("log_in")
        response = self.client.post(
            url, {"email": "ghost@example.com", "password": PASSWORD}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        url = reverse("token_refresh")
        refresh = str(RefreshToken.for_user(self.user))
        response = self.client.post(url, {"refresh": refresh}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
