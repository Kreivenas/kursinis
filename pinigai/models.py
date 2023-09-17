from django.db import models
from django.contrib.auth.models import User, BaseUserManager
from django.urls import reverse
from PIL import Image
from django.conf import settings


class CustomUserManager(BaseUserManager):
    pass


class Family(models.Model):
    name = models.CharField(max_length=255, unique=True)
    user = models.ManyToManyField(User, related_name='families')  # Pakeičiame ForeignKey į ManyToManyField

    def __str__(self):
        return self.name  


class Profile(models.Model):
    user_families = models.OneToOneField(User, on_delete=models.CASCADE)
    pareigos = models.CharField(max_length=100)
    families = models.ManyToManyField(Family, related_name='members', blank=True)
    photo = models.ImageField(default="profile_pics/default.jpeg", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user_families.username} profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)
# Create your models here.


class SharedBudget(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
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
