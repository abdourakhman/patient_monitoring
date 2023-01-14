from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from monitoring.models import Patient,Secretaire,Docteur,Salle,Service,Lit,Ordonnance,DossierMedical,RendezVous
# Register your models here.

personnelMedical=[Patient,Secretaire,Docteur,Salle,Service,Lit,Ordonnance,DossierMedical,RendezVous]



# class UserCreationForm(UserCreationForm):
#     nom = forms.CharField()
#     prenom = forms.CharField()
#     class Meta(UserCreationForm.Meta):
#         fields = UserCreationForm.Meta.fields + ('prenom', 'nom')

# class UtlisateurAdmin(UserAdmin):
#     add_form = UserCreationForm

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'first_name', 'last_name','password1', 'password2'),
#         }),
#     )


class AdminLit(admin.ModelAdmin):
    list_display = ('numero','salle','statut')

class AdminSalle(admin.ModelAdmin):
    list_display=('nom','service','statut')

class AdminService(admin.ModelAdmin):
    list_display=('nom',)

class AdminPatient(admin.ModelAdmin):
    list_display=('prenom','nom','sexe','telephone','symptoms','admission')
class AdminDocteur(admin.ModelAdmin):
    list_display=('prenom','nom','sexe','service')

class AdminRV(admin.ModelAdmin):
    list_display=('date','motif','priorite','patients','docteur')
#admin.site.unregister(User)
admin.site.register(Lit,AdminLit)
admin.site.register(Salle,AdminSalle)
admin.site.register(Service)
admin.site.register(Patient,AdminPatient)
admin.site.register(Secretaire)
admin.site.register(Docteur,AdminDocteur)
admin.site.register(DossierMedical)
admin.site.register(Ordonnance)
admin.site.register(RendezVous,AdminRV)
#admin.site.register(User, UtlisateurAdmin)