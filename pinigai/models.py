from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, User
from django.urls import reverse
from PIL import Image
from django.conf import settings

class CustomUserManager(UserManager):
    pass

class Family(models.Model):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='families_as_members', blank=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='families_as_user', blank=True)
    selected_family = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    vardas = models.CharField(max_length=255)
    pareigos = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, blank=True, related_name='family_members')
    selected_family = models.ForeignKey(Family, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.username
class Meta:
    swappable = 'AUTH_USER_MODEL'

    



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(
        default="profile_pics/default.jpeg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
# Create your models here.


class SharedBudget(models.Model):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Bendras Biudžetas: {self.balance}"


class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, blank=True)  # Šis laukas rodo į šeimą, kuriai priklauso pajama.
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Income - {self.description}"
    

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, blank=True)  # Šis laukas rodo į šeimą, kuriai priklauso pajama.    
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Expense - {self.description}"
