from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from .forms import  UserUpdateForm, ProfileUpdateForm, IncomeForm, expenseForm, CustomUserRegistrationForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile, CustomUser, Budget, Income, Expense
from .serializers import PostSerializer
from rest_framework import generics

def index(request):    
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)


def register(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Vartotojas {username} užregistruotas!')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'register.html', {'form': form})


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

class PostList(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = PostSerializer

class PostList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = PostSerializer   


@login_required
def budget(request): 
    user_budget, created = Budget.objects.get_or_create(user=request.user, defaults={'balance': 0})
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'budget.html', {'user_budget': user_budget, 'incomes': incomes, 'expenses': expenses})



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
            budget = Budget.objects.get(user=request.user)
            budget.balance += income.amount
            budget.save()
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

            expense = Expense(user=request.user, description=description, amount=amount, date=date)
            expense.save()

            budget, created = Budget.objects.get_or_create(user=request.user, defaults={'balance': 0})
            budget.balance -= expense.amount
            budget.save()

            return redirect('budget')
    else:
        form = expenseForm()

    context = {
        'expense_form': form,
    }
    return render(request, 'add_expense.html', context=context)




