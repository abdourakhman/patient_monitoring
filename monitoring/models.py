import datetime
from django.db import models
from django.contrib.auth.models import User
import time

departments=[('Cardiologie', 'Cardiologue'), ('Dermatologie', 'Dermatologue'), ('Urgence', 'Urgentiste'), ('Allergie/Immunologie', 'Allergiste/Immunologiste'), ('Chirurgie', 'Anesthesiste'), ('Biologie', 'Biologiste'), ('Radiologie', 'Radiologue'), ('Ophtalmologie', 'Ophtalmologue'), ('Odontologie', 'Dentiste'), ('Pharmacie', 'Pharmacien'), ('Consultation', 'Généraliste'), ('Laboratoire', 'Chimiste'), ('Reanimation', 'Chirurgien')]
services=[('Cardiologie', 'Cardiologie'), ('Dermatologie', 'Dermatologie'), ('Urgence', 'Urgence'), ('Allergie/Immunologie', 'Allergie/Immunologie'), ('Chirurgie', 'Chirurgie'), ('Radiologie', 'Radiologie'), ('Radiologie', 'Radiologie'), ('Ophtalmologie', 'Ophtalmologie'), ('Odontologie', 'Odontologie'), ('Pharmacie', 'Pharmacie'), ('Consultation', 'Consultation'), ('Laboratoire', 'Laboratoire'), ('Reanimation', 'Reanimation')]


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_patient')
    prenom = models.CharField(max_length=40)
    nom = models.CharField(max_length=40)
    naissance = models.DateField(null=True)
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')], null=True)
    telephone = models.CharField(max_length=20, null=False)
    symptoms = models.CharField(max_length=200,null=True)
    groupe_sanguin = models.CharField(max_length=10, null=True)
    secretaire = models.ForeignKey("Secretaire", on_delete=models.DO_NOTHING, null=True, related_name='patients')
    admission=models.DateTimeField(null=True)
    services = models.ManyToManyField("Service", related_name='patients')
    profile = models.ImageField(upload_to='profile_pic/PatientProfilePic/', null=True, blank=True)
    status=models.BooleanField(default=False)


    
    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Docteur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_docteur')
    prenom = models.CharField(max_length=40,null=False)
    nom = models.CharField(max_length=40,null=False)
    age = models.PositiveIntegerField(null=True)
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')], null=True)
    telephone = models.CharField(max_length=20, null=False)
    adresse = models.CharField(max_length=40)
    specialite = models.CharField(max_length=50,choices=departments,default='Généraliste')
    profile = models.ImageField(upload_to='profile_pic/DocteurProfilePic/', null=True, blank=True)
    service = models.ForeignKey("Service", on_delete=models.SET_DEFAULT,null=False,default=0)
    status=models.BooleanField(default=False)
    def get_full_name(self):
        return f"{self.prenom} {self.nom}"


    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Secretaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_secretaire')
    prenom = models.CharField(max_length=40)
    nom = models.CharField(max_length=40)
    age = models.PositiveIntegerField(null=True)
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')], null=True)
    telephone = models.CharField(max_length=20, null=False)
    adresse = models.CharField(max_length=40)
    profile = models.ImageField(upload_to='profile_pic/SecretaireProfilePic/', null=True, blank=True)
    status=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Salle(models.Model):
    nom = models.CharField(max_length=10, unique=True)
    statut = models.BooleanField(default=True)
    service = models.ForeignKey("Service", on_delete=models.CASCADE, related_name='salles')
    def __str__(self):
        return f"Salle {self.nom}"


class Service(models.Model):
    nom = models.CharField(max_length=50,choices=departments,default='Consultation')
    def __str__(self):
        return f"{self.nom}"

class Lit(models.Model):
    numero = models.PositiveIntegerField(unique=True,null=False)
    salle = models.ForeignKey("Salle", on_delete=models.SET_DEFAULT,default=0,related_name='lits')
    statut = models.BooleanField(null=False,default=True)
    
    def __str__(self):
        return f"lit N°{self.numero}/{self.salle}"

class Ordonnance(models.Model):
    contenu = models.TextField(null=False)
    docteur = models.ForeignKey("Docteur", on_delete=models.CASCADE, related_name='docteurs', null=True)
    date = models.DateField(auto_now=True)
    dossier_medical = models.ForeignKey("DossierMedical", on_delete=models.CASCADE, related_name='ordonnances', null=True)

    def __str__(self):
        return f"ordonnace docteur {self.docteur}"

class DossierMedical(models.Model):
    numero = models.CharField(max_length=50, unique=True, null=False)
    creation = models.DateField(auto_now=True)
    miseAjour = models.DateField(auto_now_add=True)
    service = models.ForeignKey("Service", on_delete=models.CASCADE, related_name='dossiers', null=True)
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE, related_name='patients')

    def __str__(self):
        return f"Dossier n°{self.numero}/ {self.service}"

class RendezVous(models.Model):
    date = models.DateTimeField(null=False)
    heure = models.TimeField(null=False,default=datetime.time(8, 0))
    motif = models.CharField(max_length=255, null=True, default="Aucun motif particulier")
    priorite = models.CharField(max_length=7, null=False,choices=[('Urgent','Urgent'),('Moyen','Moyen'),('Faible','Faible')],default='Moyen')
    docteur = models.ForeignKey("Docteur", on_delete=models.CASCADE,related_name='rendez_vous_docteur')
    patients = models.ForeignKey("Patient", on_delete=models.DO_NOTHING,related_name='rendez_vous_patient')

    def __str__(self):
        return f"{self.date}"

class Docteur_Patient:
    docteur = models.ForeignKey("Docteur", on_delete=models.CASCADE,related_name='docteur_patient')
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE,related_name='docteur_patient')

class Patient_Service:
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE,related_name='patient_service')
    docteur = models.ForeignKey("Docteur", on_delete=models.CASCADE,related_name='docteur_patient2')






