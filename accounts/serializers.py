from rest_framework import serializers
from .models import CustomUser, APIClient

class APIClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIClient
        fields = ["client_id", "token", "created_at", "expires_at"]

class AdminUserSerializer(serializers.ModelSerializer):
    api_client = APIClientSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "is_staff", "api_client"]
