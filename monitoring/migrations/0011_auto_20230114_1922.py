# Generated by Django 3.0.5 on 2023-01-14 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0010_auto_20230114_1908'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='admission',
            field=models.DateTimeField(default='10 janvier 2023 19:15'),
        ),
    ]
