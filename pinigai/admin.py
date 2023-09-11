from django.contrib import admin
from .models import Profile, CustomUser, SharedBudget, Income, Expense


admin.site.register(Profile)
admin.site.register(CustomUser)
admin.site.register(SharedBudget)
admin.site.register(Income)
admin.site.register(Expense)




# Register your models here.
