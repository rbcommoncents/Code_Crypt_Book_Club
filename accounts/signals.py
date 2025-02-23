from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import APIClient, CustomUser

@receiver(post_save, sender=CustomUser)
def create_api_client(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        APIClient.objects.create(user=instance)
