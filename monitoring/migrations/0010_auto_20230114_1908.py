# Generated by Django 3.0.5 on 2023-01-14 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0009_auto_20230114_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='admission',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='rendezvous',
            name='date',
            field=models.DateTimeField(),
        ),
    ]