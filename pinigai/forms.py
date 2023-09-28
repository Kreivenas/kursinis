from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Family
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']


class IncomeForm(forms.Form):
    Paskirtis = forms.CharField(max_length=255)
    Suma = forms.DecimalField(max_digits=10, decimal_places=2)
    Data = forms.DateField()



class expenseForm(forms.Form):
    Paskirtis = forms.CharField(max_length=255)
    Suma = forms.DecimalField(max_digits=10, decimal_places=2)
    Data = forms.DateField()

class FamilyCreationForm(forms.ModelForm):
    description = forms.CharField(max_length=255)
    class Meta:
        model = Family
        fields = ['name', 'users' ]  # Pridėkite laukus pagal poreikį.

class FamilySelectionForm(forms.Form):
    # selected_family = forms.ModelChoiceField(
    #     queryset=Family.objects.all(),  # Gauname visus šeimos objektus
    #     empty_label="Pasirinkite šeimą",  # Tekstas pradiniam pasirinkimui
    #     required=False,  # Nereikalingas privalomas pasirinkimas
    #     widget=forms.Select(attrs={'class': 'form-control'}),  # Paprastas pasirinkimo langelis su stiliais
    # )
    new_family_name = forms.CharField(
        max_length=255,
        required=False,  # Nereikalingas privalomas laukas
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Įveskite naujo fondo pavadinimą'}),  # Teksto laukas su stiliais
    )

class AddUserToFamilyForm(forms.Form):
    username = forms.CharField(label='Username')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('User does not exist.')
        return username