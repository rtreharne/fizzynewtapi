# Generated by Django 3.2.9 on 2023-07-18 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0022_auto_20230708_0608'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='group_fnid',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
