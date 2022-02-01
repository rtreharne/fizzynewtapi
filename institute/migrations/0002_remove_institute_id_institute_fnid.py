# Generated by Django 4.0.1 on 2022-02-01 09:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institute',
            name='id',
        ),
        migrations.AddField(
            model_name='institute',
            name='fnid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
