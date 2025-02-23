import uuid
import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils.timezone import now
from rest_framework.authtoken.models import Token

def user_profile_picture_path(instance, filename):
    ext = filename.split(".")[-1] 
    new_filename = f"profile_{uuid.uuid4().hex}.{ext}" 
    return os.path.join("profile_pics/", new_filename) 

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True) 
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True, null=True)

    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ["username"] 

    def __str__(self):
        return self.email

    @property
    def aws_profile_picture_url(self):
        if self.profile_picture:
            return f"{settings.MEDIA_URL}{self.profile_picture}"
        return None

class APIClient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="api_client")
    client_id = models.CharField(max_length=255, unique=True)
    token = models.CharField(max_length=255, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def sync_with_drf_token(self):
        drf_token, _ = Token.objects.get_or_create(user=self.user)  
        self.save()

    def regenerate_token(self):
        Token.objects.filter(user=self.user).delete()

        new_token = Token.objects.create(user=self.user)
        self.token = new_token.key 

        self.created_at = now()
        self.save()

        return self.token 

    def __str__(self):
        return f"{self.user.username} API Access (Token: {self.token})"