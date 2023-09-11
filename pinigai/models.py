from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, User
from django.urls import reverse
from PIL import Image
from django.conf import settings

# from tinymce.models import HTMLField
class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    vardas = models.CharField(max_length=255)
    pareigos = models.CharField(max_length=100)
    email = models.EmailField(unique=False) 

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['vardas', 'email']  
    objects = CustomUserManager()

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
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Income - {self.description}"
    

class Expense(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Expense - {self.description}"
