# Generated by Django 3.2.9 on 2023-07-08 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0021_alter_attendance_institute_fnid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='course_instance_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='group_fnid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='programme_fnid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='school_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='session_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='session_type_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='student_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='session',
            name='course_instance_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='session',
            name='institute_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='session',
            name='session_type_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='sessionrequest',
            name='course_instance_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='sessionrequest',
            name='institute_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='sessionrequest',
            name='session_fnid',
            field=models.UUIDField(null=True),
        ),
        migrations.AlterField(
            model_name='sessionrequest',
            name='session_type_fnid',
            field=models.UUIDField(),
        ),
        migrations.AlterField(
            model_name='sessionrequest',
            name='student_fnid',
            field=models.UUIDField(),
        ),
    ]