# Generated by Django 4.0.1 on 2022-02-06 07:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('fnid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('institute_fnid', models.CharField(max_length=128)),
                ('code', models.CharField(help_text='(e.g. MATH101)', max_length=9)),
                ('name', models.CharField(max_length=128)),
                ('visible', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
