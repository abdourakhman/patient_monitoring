# Generated by Django 3.0.5 on 2023-01-15 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0013_auto_20230114_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='rendezvous',
            name='heure',
            field=models.TimeField(default='08:00'),
        ),
        migrations.AlterField(
            model_name='rendezvous',
            name='date',
            field=models.DateField(),
        ),
    ]