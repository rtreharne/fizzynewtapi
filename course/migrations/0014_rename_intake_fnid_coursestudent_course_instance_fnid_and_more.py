# Generated by Django 4.0.1 on 2022-05-19 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0013_remove_course_duration_weeks_remove_course_repeat_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coursestudent',
            old_name='intake_fnid',
            new_name='course_instance_fnid',
        ),
        migrations.AddField(
            model_name='courseinstance',
            name='visible',
            field=models.BooleanField(default=True),
        ),
    ]