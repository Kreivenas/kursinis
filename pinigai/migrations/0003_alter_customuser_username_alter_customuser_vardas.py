# Generated by Django 4.2.4 on 2023-08-30 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pinigai', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='vardas',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
