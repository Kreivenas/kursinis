from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Sum
from django.shortcuts import redirect
from .forms import  UserUpdateForm, ProfileUpdateForm, IncomeForm, expenseForm, CustomUserRegistrationForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile, CustomUser, SharedBudget, Income, Expense
from .serializers import PostSerializer
from rest_framework import generics

def index(request):    

    return render(request, 'index.html')


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
def budget_page(request):
    shared_budget, created = SharedBudget.objects.get_or_create(pk=1, defaults={'balance': 0})
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    total_income_amount = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    return render(request, 'budget.html', {'shared_budget': shared_budget, 'incomes': incomes, 'expenses': expenses, 'total_income_amount': total_income_amount, 'total_expense_amount': total_expense_amount})



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






