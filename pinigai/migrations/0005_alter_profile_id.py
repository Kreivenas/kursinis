# Generated by Django 4.2.4 on 2023-09-25 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinigai', '0004_alter_expense_user_alter_income_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]