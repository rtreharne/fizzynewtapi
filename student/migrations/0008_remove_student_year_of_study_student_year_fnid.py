# Generated by Django 4.0.1 on 2022-05-24 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_studentemail_institute_fnid_studentemail_primary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='year_of_study',
        ),
        migrations.AddField(
            model_name='student',
            name='year_fnid',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
