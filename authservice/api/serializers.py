from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    # write_only keeps the password out of responses; validate_password enforces
    # the project's AUTH_PASSWORD_VALIDATORS (min length, common, numeric).
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    # email is the login identifier: allow partial updates but never blank it out.
    email = serializers.EmailField(required=False, allow_null=False)

    class Meta:
        model = User
        fields = ["id", "username", "email"]

    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.save()
        return instance


class LoginSerializer(TokenObtainPairSerializer):
    """Adds non-sensitive user fields as custom claims on the JWT."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != "id":
                token[key] = value
        return token
