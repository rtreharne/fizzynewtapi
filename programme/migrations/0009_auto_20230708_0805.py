# Generated by Django 3.2.9 on 2023-07-08 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0008_programme_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='institute_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='programme',
            name='school_fnid',
            field=models.UUIDField(),
        ),
    ]
