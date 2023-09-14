from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile, Family
from django import forms
from django.contrib.auth.models import User


class CustomUserRegistrationForm(UserCreationForm):
    vardas = forms.CharField(max_length=255)
    pareigos = forms.CharField(max_length=100)
    email = forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    family = forms.ModelChoiceField(queryset=Family.objects.all())
    class Meta:
        model = CustomUser
        fields = ['vardas', 'pareigos', 'email', 'username', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']       


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class IncomeForm(forms.Form):
    description = forms.CharField(max_length=255)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    date = forms.DateField()
    


class expenseForm(forms.Form):
    description = forms.CharField(max_length=255)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    date = forms.DateField()
   
class FamilyCreationForm(forms.ModelForm):
    description = forms.CharField(max_length=255)
    class Meta:
        model = Family
        fields = ['name', 'members' ]  # Pridėkite laukus pagal poreikį.

class FamilySelectionForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['selected_family']