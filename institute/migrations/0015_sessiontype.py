# Generated by Django 4.0.1 on 2022-11-26 08:44

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0014_year_next_year_fnid_year_previous_year_fnid'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionType',
            fields=[
                ('fnid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('institute_fnid', models.CharField(max_length=128)),
                ('label', models.CharField(max_length=128)),
            ],
            options={
                'unique_together': {('institute_fnid', 'label')},
            },
        ),
    ]
