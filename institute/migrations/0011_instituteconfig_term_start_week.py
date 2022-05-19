# Generated by Django 4.0.1 on 2022-05-18 11:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0010_alter_institutedomain_domain'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituteconfig',
            name='term_start_week',
            field=models.PositiveIntegerField(default=35, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(52)]),
        ),
    ]
