# Generated by Django 4.2.4 on 2023-09-18 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinigai', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='family',
            old_name='user',
            new_name='users',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='user_families',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='families',
        ),
        migrations.AddField(
            model_name='family',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='SharedBudget',
        ),
    ]
