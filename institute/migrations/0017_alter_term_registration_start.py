# Generated by Django 4.0.1 on 2023-05-24 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0016_alter_term_end_date_alter_term_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='registration_start',
            field=models.DateTimeField(),
        ),
    ]