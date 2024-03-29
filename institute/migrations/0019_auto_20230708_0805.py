# Generated by Django 3.2.9 on 2023-07-08 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0018_term_current'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instituteconfig',
            name='institute_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='sessiontype',
            name='institute_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='term',
            name='institute_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='year',
            name='institute_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='year',
            name='next_year_fnid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='year',
            name='previous_year_fnid',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
