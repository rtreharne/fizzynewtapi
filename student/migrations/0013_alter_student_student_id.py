# Generated by Django 4.0.1 on 2022-05-25 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_student_undergraduate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_id',
            field=models.CharField(blank=True, default=None, max_length=12, null=True),
        ),
    ]
