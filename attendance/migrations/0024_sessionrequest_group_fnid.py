# Generated by Django 3.2.9 on 2023-07-24 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0023_session_group_fnid'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionrequest',
            name='group_fnid',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
