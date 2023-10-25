from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import redirect
from .forms import LoginForm, RegisterForm, AddUserToFamilyForm, FamilyCreationForm, UserUpdateForm, ProfileUpdateForm, IncomeForm, expenseForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Income, Expense, Family
from rest_framework import generics
import logging
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.db import IntegrityError




def index(request):
    return render(request, 'index.html')

# def create_new_family(user, family_name):
#     family = Family.objects.create(name=family_name)
#     family.user.add(user)  # Pridėkite vartotoją prie šeimos
#     return family

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.title()
            user.save()
            messages.success(request, 'Atlikote sėkmingą registraciją.')
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})


def sign_in(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('profile')


        form = LoginForm()
        return render(request,'login.html', {'form': form})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Labas {username.title()}, Malonu Tave Matyti!')
                return redirect('profile')

        messages.error(request,f'Neteisingas naudotojo vardas arba slaptažodis.')
        return render(request,'login.html',{'form': form})


def sign_out(request):
    logout(request)
    messages.success(request,f'Jūs esate atsijungęs.')
    return redirect('login')

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    user_families = request.user.families.all()

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_families': user_families
    }

    return render(request, 'profile.html', context=context)


@login_required
def view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_families = user.families.all()
    return render(request, 'profiles.html', {'user': user, 'user_families': user_families})



@login_required
def select_family(request):
    new_family = None
    user_families = request.user.families.all()

    if request.method == 'POST':
        form = FamilyCreationForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            expiration_date = form.cleaned_data.get('expiration_date')

            if name:
                try:
                    family = Family.objects.get(name=name)
                    messages.error(request, 'Toks fondas jau egzistuoja.')
                    return redirect('profile')
                except Family.DoesNotExist:
                    new_family = Family.objects.create(name=name, expiration_date=expiration_date)
                    new_family.users.add(request.user)
                    request.user.families.add(new_family)
                    messages.success(request, 'Sukurtas naujas fondas.')
                    return redirect('profile')
    else:
        form = FamilyCreationForm()

    return render(request, 'family_selection_form.html', {'form': form, 'new_family': new_family, 'user_families': user_families})


@login_required
def budget_page(request, family_id):
    family = get_object_or_404(Family, id=family_id)

    if not request.user.families.filter(id=family_id).exists():
        return HttpResponseForbidden("Prieiga uždrausta")



    incomes = Income.objects.filter(family=family)
    expenses = Expense.objects.filter(family=family)

    total_income_amount = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    add_user_form = AddUserToFamilyForm()
    users = family.users.all()

    return render(request, 'budget.html', {
        'incomes': incomes,
        'expenses': expenses,
        'total_income_amount': total_income_amount,
        'total_expense_amount': total_expense_amount,
        'family': family,
        'add_user_form': add_user_form,
        'users': users
    })

@login_required
def add_user_to_family(request, family_id):
    family = get_object_or_404(Family, id=family_id)

    if request.method == 'POST':
        form = AddUserToFamilyForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user_to_add = User.objects.get(username=username)
            family.users.add(user_to_add)
            messages.success(request, f'{username} Pridėtas prie fondo".')
            return redirect('budget', family_id=family_id)
    else:
        form = AddUserToFamilyForm()

    return render(request, 'add_user_to_family.html', {'form': form, 'family': family})

def family_users(request, family_id):
    family = get_object_or_404(Family, id=family_id)
    users = family.users.all()
    return render(request, 'family_users.html', {'users': users})

@login_required
def leave_family(request, family_id):
    family = get_object_or_404(Family, id=family_id)

    if request.user.families.filter(id=family_id).exists():
        family.users.remove(request.user)
        messages.success(request, 'Jūs sėkmingai palikote fondą.')
    else:
        messages.error(request, 'Jūs nepriklausote šiam fondui.')

    return redirect('profile')

@login_required
def delete_family(request, family_id):
    family = get_object_or_404(Family, id=family_id)

    if request.user in family.users.all():
        if request.user == family.users.first():
            family.delete()
            messages.success(request, 'Fondas ištrinta sėkmingai.')
        else:
            messages.error(request, 'Neturite leidimo ištrinti šio fondo.')
    else:
        messages.error(request, 'Neturite leidimo ištrinti šio fondo.')

    return redirect('profile')

@login_required
def add_income(request, family_id):
    family = get_object_or_404(Family, id=family_id)

    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            amount = form.cleaned_data['amount']
            date = form.cleaned_data['date']

            income = Income(user=request.user, family=family, description=description, amount=amount, date=date)
            income.save()

            family.balance += amount
            family.save()

            return redirect('budget', family_id=family_id)

    else:
        form = IncomeForm()
    context = {
        'income_form': form,
        'family_id': family_id,
    }
    return render(request, 'add_income.html', context=context)


@login_required
def add_expense(request, family_id):
    family = get_object_or_404(Family, id=family_id)

    if request.method == "POST":
        form = expenseForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            amount = form.cleaned_data['amount']
            date = form.cleaned_data['date']

            expense = Expense(user=request.user, family=family, description=description, amount=amount, date=date)
            expense.save()

            family.balance -= amount
            family.save()

            return redirect('budget', family_id=family_id)

    else:
        form = expenseForm()

    context = {
        'expense_form': form,
        'family_id': family_id,
    }
    return render(request, 'add_expense.html', context=context)







