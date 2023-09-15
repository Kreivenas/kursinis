from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('register/', views.sign_up, name='register'),
    path('profile/', views.profile, name='profile'),
    path('budget/', views.budget_page, name='budget'),
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('family_form/', views.create_family, name='create_family_form'),
    path('select_family/', views.select_family, name='select_family'),
    path('family/', views.family_page, name='family_page'),
]
