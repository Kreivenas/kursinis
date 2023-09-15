from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import redirect
from .forms import LoginForm, RegisterForm, FamilyCreationForm, FamilySelectionForm, UserUpdateForm, ProfileUpdateForm, IncomeForm, expenseForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile, SharedBudget, Income, Expense
from rest_framework import generics
import logging
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout



def index(request):    
    return render(request, 'index.html')


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'users/register.html', {'form': form})


def sign_in(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('profile')


        form = LoginForm()
        return render(request,'users/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('profile')
        
        # form is not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'users/login.html',{'form': form})
    

def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login')       

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
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
    }

    return render(request, 'profile.html', context)


@login_required
def family_page(request):
    return render(request, 'family.html')

logging.basicConfig(level=logging.INFO)

@login_required
def select_family(request):
    if request.method == 'POST':
        form = FamilySelectionForm(request.POST)
        if form.is_valid():
            if 'selected_family' in form.cleaned_data:
                selected_family = form.cleaned_data['selected_family']
                print("Pasirinkta šeima")
                selected_family.user.add(request.user)
                logging.info("Priskirtas vartotojas prie šeimos.")
                return redirect('budget')

    else:
        form = FamilySelectionForm()
    
    return render(request, 'family_selection_form.html', {'form': form})

@login_required
def create_family(request):
    if request.method == "POST":
        form = FamilyCreationForm(request.POST)
        if form.is_valid():
            family = form.save()
            family.user.add(request.user)
            return redirect('profile')
    else:
        form = FamilyCreationForm()

    return render(request, 'create_family_form.html', {'form': form})



@login_required
def budget_page(request):
    user_family = request.user.family
    if user_family:
        # Gauti šeimos narius
        family_user = user_family.user.all()
        print("Šeimos objektas:", user_family)


        # Gauti ar sukurti bendrą biudžetą šeimai
        shared_budget, created = SharedBudget.objects.get_or_create(family=user_family, defaults={'balance': 0})

        # Gauti vartotojo pajamas ir išlaidas šeimoje
        incomes = Income.objects.filter(user=request.user, family=user_family)
        expenses = Expense.objects.filter(user=request.user, family=user_family)

        # Apskaičiuoti vartotojo visų pajamų ir išlaidų sumas
        total_income_amount = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

        return render(request, 'budget.html', {
            'family_user': family_user,
            'shared_budget': shared_budget,
            'incomes': incomes,
            'expenses': expenses,
            'total_income_amount': total_income_amount,
            'total_expense_amount': total_expense_amount,
        })
    else:
        # Vartotojas nepriklauso jokiai šeimai, tai galite nukreipti jį į šeimų kūrimo puslapį arba pridėti kitą elgesį pagal poreikį.
        return render(request, 'no_family.html')


@login_required
def add_income(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            amount = form.cleaned_data['amount']
            date = form.cleaned_data['date']
            income = Income(user=request.user, description=description, amount=amount, date=date)
            income.save()

            # Atnaujiname bendrą biudžetą tik tuomet, kai sukuriamas naujas pajamų įrašas
            shared_budget, created = SharedBudget.objects.get_or_create(pk=1, defaults={'balance': 0})
            shared_budget.balance += income.amount
            shared_budget.save()

            return redirect('budget')
    else:
        form = IncomeForm()
    context = {
        'income_form': form
    }
    return render(request, 'add_income.html', context=context)



@login_required
def add_expense(request):
    if request.method == "POST":
        form = expenseForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            amount = form.cleaned_data['amount']
            date = form.cleaned_data['date']
            
            # Sukurkite naują išlaidų įrašą
            expense = Expense(user=request.user, description=description, amount=amount, date=date)
            expense.save()

            # Atnaujinkite bendrą biudžetą tik tuomet, kai sukuriamas naujas išlaidų įrašas
            shared_budget, created = SharedBudget.objects.get_or_create(pk=1, defaults={'balance': 0})
            shared_budget.balance -= expense.amount
            shared_budget.save()

            return redirect('budget')
    else:
        form = expenseForm()

    context = {
        'expense_form': form,
    }
    return render(request, 'add_expense.html', context=context)






