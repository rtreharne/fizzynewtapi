# Generated by Django 4.0.1 on 2022-05-18 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0005_programme_term_start_date_override'),
    ]

    operations = [
        migrations.RenameField(
            model_name='programme',
            old_name='term_start_date_override',
            new_name='term_start_week_override',
        ),
    ]
