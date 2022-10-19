# Generated by Django 4.0.1 on 2022-04-05 12:04

import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_course_duration_weeks_course_repeat_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseIntake',
            fields=[
                ('fnid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('institute_fnid', models.CharField(max_length=128)),
                ('course_fnid', models.CharField(max_length=128)),
                ('start', models.DateField()),
                ('duration_weeks', models.IntegerField(default=52, validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='coursestudent',
            name='intake_fnid',
            field=models.CharField(default='', max_length=128),
        ),
    ]