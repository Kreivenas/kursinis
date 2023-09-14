# Generated by Django 4.2.4 on 2023-09-14 17:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinigai', '0013_remove_family_parent_family'),
    ]

    operations = [
        migrations.AddField(
            model_name='family',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='families_as_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='family',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='families_as_members', to=settings.AUTH_USER_MODEL),
        ),
    ]