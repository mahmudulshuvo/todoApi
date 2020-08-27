from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

# Create your models here.

class JwtSecret(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    jwt_secret = models.UUIDField(default=uuid.uuid4)


class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

@receiver(post_save, sender=User)
def create_user_jwtsecret(sender, instance, created, **kwargs):
    if created:
        JwtSecret.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_jwtsecret(sender, instance, **kwargs):
    instance.jwtsecret.save()


def jwt_get_secret_key(user_model):
    return user_model.jwtsecret.jwt_secret
