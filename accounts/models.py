from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Use email as a unique identifier
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    USERNAME_FIELD = "email"  # Login with email instead of username
    REQUIRED_FIELDS = ["username"]  # Username is still required

    def __str__(self):
        return self.email
