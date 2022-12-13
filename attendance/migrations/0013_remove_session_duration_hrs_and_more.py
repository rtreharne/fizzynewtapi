# Generated by Django 4.0.1 on 2022-12-13 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0012_sessionrequest_session_fnid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='duration_hrs',
        ),
        migrations.RemoveField(
            model_name='sessionrequest',
            name='duration_hrs',
        ),
        migrations.AddField(
            model_name='session',
            name='duration_mins',
            field=models.IntegerField(default=60),
        ),
        migrations.AddField(
            model_name='sessionrequest',
            name='duration_mins',
            field=models.IntegerField(default=60),
        ),
    ]
