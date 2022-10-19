# Generated by Django 4.0.1 on 2022-10-19 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0020_courseinstance_last_session_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courseinstance',
            options={'ordering': ('-created_at',)},
        ),
        migrations.AlterUniqueTogether(
            name='courseinstance',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='courseinstance',
            name='name_override',
            field=models.CharField(max_length=128),
        ),
    ]
