# Generated by Django 4.0.1 on 2022-02-04 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0002_institutedomain_remove_institute_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='institutedomain',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='institutedomain',
            unique_together={('institute_fnid', 'domain')},
        ),
    ]
