from django import forms
from django.contrib.auth.models import User
from . import models


#for user related form
class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

#for doctor related form
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Docteur
        fields=['prenom','nom','age','sexe','telephone','adresse','specialite','service','profile']
       


class AssistantForm(forms.ModelForm):
    class Meta:
        model=models.Secretaire
        fields=['prenom','nom','age','sexe','telephone','adresse','profile']
       

# #for admin signup
# class AdminSigupForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','username','password']
#         widgets = {
#         'password': forms.PasswordInput()
#         }


# #for student related form
# class DoctorUserForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['first_name','last_name','username','password']
#         widgets = {
#         'password': forms.PasswordInput()
#         }
# class DoctorForm(forms.ModelForm):
#     class Meta:
#         model=models.Docteur
#         fields=['adresse','prenom','nom','specialite','profile']



#for patient related form
class PatientForm(forms.ModelForm):
    class Meta:
        model=models.Patient
        fields=['prenom','nom','naissance','sexe','telephone','symptoms','groupe_sanguin','secretaire','services', 'profile']
        widgets = {'naissance':forms.DateInput()}


# # class AppointmentForm(forms.ModelForm):
# #     doctorId=forms.ModelChoiceField(queryset=models.Docteur.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
# #     patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Patient Name and Symptoms", to_field_name="user_id")
# #     class Meta:
# #         model=models.Appointment
# #         fields=['description','status']


# # class PatientAppointmentForm(forms.ModelForm):
# #     doctorId=forms.ModelChoiceField(queryset=models.Docteur.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
# #     class Meta:
# #         model=models.Appointment
# #         fields=['description','status']


#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))

class Rendez_vousForm(forms.ModelForm):
    class Meta:
        model=models.RendezVous
        fields=['date','heure','motif','priorite','docteur','patients']
        widgets = {
            'docteur': forms.TextInput(attrs={'disabled': 'disabled'}),
        }

#For prescription
class OrdonnanceForm(forms.ModelForm):
    class Meta:
        model=models.Ordonnance
        fields = ['contenu', 'docteur', 'dossier_medical'] 
        # widgets = {'docteur': forms.TextInput(attrs={'disabled': 'disabled'}),
        # }


class DossierForm(forms.ModelForm):
    class Meta:
        model = models.DossierMedical
        fields = ['numero', 'service', 'patient']
        widgets = {'service': forms.TextInput(attrs={'disabled': 'disabled'}),}

