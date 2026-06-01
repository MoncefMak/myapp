from django.test import TestCase

from accounts.models import User


class UserModelTests(TestCase):
    """Tests for the custom User model and its email-keyed manager."""

    def test_email_is_normalized_on_save(self):
        user = User.objects.create_user(
            username="normalize",
            email="  Foo@Bar.COM ",
            password="Str0ngPass!42",
        )
        user.refresh_from_db()
        self.assertEqual(user.email, "foo@bar.com")

    def test_create_user_requires_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                username="noemail", email="", password="Str0ngPass!42"
            )

    def test_create_user_defaults(self):
        user = User.objects.create_user(
            username="plain", email="plain@example.com", password="Str0ngPass!42"
        )
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password("Str0ngPass!42"))

    def test_create_superuser_sets_flags(self):
        admin = User.objects.create_superuser(
            username="boss", email="boss@example.com", password="Str0ngPass!42"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_active)

    def test_str_representation(self):
        user = User.objects.create_user(
            username="repr", email="repr@example.com", password="Str0ngPass!42"
        )
        self.assertEqual(str(user), "repr <repr@example.com>")
