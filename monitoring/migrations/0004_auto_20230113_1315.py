# Generated by Django 3.0.5 on 2023-01-13 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0003_auto_20230113_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='docteur',
            name='specialite',
            field=models.CharField(choices=[('Cardiologie', 'Cardiologue'), ('Dermatologie', 'Dermatologue'), ('Urgence', 'Urgentiste'), ('Allergie/Immunologie', 'Allergiste/Immunologiste'), ('Chirurgie', 'Anesthesiste'), ('Biologie', 'Biologiste'), ('Radiologie', 'Radiologue'), ('Ophtalmologie', 'Ophtalmologue'), ('Odontologie', 'Dentiste'), ('Pharmacie', 'Pharmacien'), ('Consultation', 'Généraliste'), ('Laboratoire', 'Chimiste'), ('Reanimation', 'Chirurgien')], default='Généraliste', max_length=50),
        ),
        migrations.AlterField(
            model_name='service',
            name='nom',
            field=models.CharField(choices=[('Cardiologie', 'Cardiologue'), ('Dermatologie', 'Dermatologue'), ('Urgence', 'Urgentiste'), ('Allergie/Immunologie', 'Allergiste/Immunologiste'), ('Chirurgie', 'Anesthesiste'), ('Biologie', 'Biologiste'), ('Radiologie', 'Radiologue'), ('Ophtalmologie', 'Ophtalmologue'), ('Odontologie', 'Dentiste'), ('Pharmacie', 'Pharmacien'), ('Consultation', 'Généraliste'), ('Laboratoire', 'Chimiste'), ('Reanimation', 'Chirurgien')], default='Consultation', max_length=50),
        ),
    ]
