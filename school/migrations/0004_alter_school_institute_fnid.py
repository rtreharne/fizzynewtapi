# Generated by Django 4.0.1 on 2022-02-10 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_alter_school_options_alter_school_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='institute_fnid',
            field=models.CharField(editable=False, max_length=128),
        ),
    ]
