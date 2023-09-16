from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Family
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    

class RegisterForm(UserCreationForm):
    pareigos = forms.CharField(max_length=100)
    family_choice = forms.ModelChoiceField(queryset=Family.objects.all(), required=False, empty_label='Select an existing family')
    new_family_name = forms.CharField(max_length=100, required=False)
    class Meta:
        model=User
        fields = ['username','email','pareigos','family_choice', 'new_family_name','password1','password2'] 

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
        fields = ['name', 'user' ]  # Pridėkite laukus pagal poreikį.

class FamilySelectionForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['name', 'user']