from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Perfil

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_user(instance, sender, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)