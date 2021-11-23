from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.dispatch import receiver
from django.db.models.signals import post_save

def get_elapse():
    return now() + timedelta(hours=48)

class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', blank=True, null=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18)

    def safe_delete(self):
        self.is_active = False
        self.save()

    activation_key = models.CharField(max_length=128, blank=True)

    def is_activation_key_expired(self):
        return now() - self.date_joined > timedelta(hours=48)


class UserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'W'
    OTHER = 'X'

    GENDER_CHOICES = (
        (MALE, 'M'),
        (FEMALE, 'Ж'),
        (OTHER, 'Х')
    )

    user = models.OneToOneField(
        User, unique=True, null=False, db_index=True, on_delete=models.CASCADE
    )

    tagline = models.CharField(verbose_name='тэги', max_length=128, blank=True)
    about_me = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='пол', max_length=1, choices=GENDER_CHOICES, blank=True)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)