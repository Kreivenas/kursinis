from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('register/', views.sign_up, name='register'),
    path('profiles/<int:user_id>/', views.view_profile, name='profiles'),
    path('profile/', views.profile, name='profile'),
    path('budget/<int:family_id>/', views.budget_page, name='budget'),
    path('add_income/<int:family_id>/', views.add_income, name='add_income'),
    path('add_expense/<int:family_id>/', views.add_expense, name='add_expense'),
    path('select_family/', views.select_family, name='select_family'),
    path('delete_family/<int:family_id>/', views.delete_family, name='delete_family'),
    path('add_user_to_family/<int:family_id>/', views.add_user_to_family, name='add_user_to_family'),
    path('leave_family/<int:family_id>/', views.leave_family, name='leave_family'),
]



    # path('family_form/', views.create_family, name='create_family_form'),
    # path('family/', views.family_page, name='family_page'),

