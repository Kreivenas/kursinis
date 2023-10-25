from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Family
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Family)
def check_family_expiration_date(sender, instance, **kwargs):
    from pinigai.tasks import delete_expired_families
    if instance.expiration_date:
        # Tikriname, ar expiration_date yra nustatytas
        delete_expired_families()