# Generated by Django 4.0.1 on 2022-05-24 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0013_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='year',
            name='next_year_fnid',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='year',
            name='previous_year_fnid',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
