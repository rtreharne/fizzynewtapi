# Generated by Django 4.0.1 on 2022-02-01 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('institute', '0002_remove_institute_id_institute_fnid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institute',
            name='fnid',
        ),
        migrations.AddField(
            model_name='institute',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
