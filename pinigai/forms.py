from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Family, Income, Expense
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Vardas')
    last_name = forms.CharField(max_length=30, required=True, help_text='Pavardė')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='Vardas', max_length=30, required=True, help_text='Vardas')
    last_name = forms.CharField(label='Pavardė', max_length=30, required=True, help_text='Pavardė')
    email = forms.CharField(label='El. paštas', max_length=30, required=True, help_text='El. paštas')
    username = forms.CharField(label='Prisijungimo vardas', max_length=30, required=True, help_text='Prisijungimo vardas')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    photo = forms.FileField(label='Nuotrauka', required=True, )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].widget.initial_text = "Esama"
        self.fields['photo'].widget.input_text = "Pakeisti"

    class Meta:
        model = Profile
        fields = ['photo']



class IncomeForm(forms.ModelForm):

    class Meta:
        model = Income
        fields = ['description', 'amount', 'date']
        labels = {
            'description': 'Paskirtis',
            'amount': 'Suma',
            'date': 'Data'
        }



class expenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date']
        labels = {
            'description': 'Paskirtis',
            'amount': 'Suma',
            'date': 'Data'
        }

class FamilyCreationForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ['name', 'expiration_date']
        labels = {
            'name': 'Fondo pavadinimas',
            'expiration_date': 'Galiojimo data'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Įveskite fondo pavadinimą'}),
            'expiration_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Pasirinkite galiojimo datą: yyyy/mm/dd'})
        }

class FamilySelectionForm(forms.Form):
    # selected_family = forms.ModelChoiceField(
    #     queryset=Family.objects.all(),
    #     empty_label="Pasirinkite šeimą",
    #     required=False,
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    # )
    new_family_name = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Įveskite naujo fondo pavadinimą'}),
    )
    expiration_date = forms.DateField(
    required=False,
    widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )

class AddUserToFamilyForm(forms.Form):
    username = forms.CharField(label='Username')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('User does not exist.')
        return username