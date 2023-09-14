from django.contrib import admin
from .models import Profile, CustomUser, SharedBudget, Income, Expense, Family


admin.site.register(Profile)
admin.site.register(CustomUser)
admin.site.register(SharedBudget)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Family)




# Register your models here.
