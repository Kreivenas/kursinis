from django.db import models
from django.contrib.auth.models import User, BaseUserManager
from django.urls import reverse
from PIL import Image
from django.conf import settings
from datetime import datetime



class CustomUserManager(BaseUserManager):
    pass


class Family(models.Model):
    name = models.CharField(max_length=255, unique=True)
    users = models.ManyToManyField(User, related_name='families')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return self.name  


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.AutoField(User, primary_key=True)
    pareigos = models.CharField(max_length=100)
    photo = models.ImageField(default="profile_pics/default.jpeg", upload_to="profile_pics")

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



class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="incomes")
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, blank=True)  
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255, default='Other')
    date = models.DateField()


    def __str__(self):
        return f"Income - {self.description}"
    

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    family = models.ForeignKey(Family, on_delete=models.SET_NULL, null=True, blank=True)  # Šis laukas rodo į šeimą, kuriai priklauso pajama.    
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255, default='Other')
    date = models.DateField()

    def __str__(self):
        return f"Expense - {self.description}"
