# Generated by Django 4.0.1 on 2022-11-28 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0011_remove_attendance_peer_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionrequest',
            name='session_fnid',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
    ]
