# Generated by Django 4.0.1 on 2022-04-04 12:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_coursestudent_institute_fnid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='threshold',
            field=models.IntegerField(default=10, validators=[django.core.validators.MaxLengthValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]