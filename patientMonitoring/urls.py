
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import admin
from django.urls import path

from monitoring import views


#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),
    path('docteur',views.interface_docteur,name='interface_docteur'),
    path('contactus', views.contactus_view),


    
    
    path('aboutus', views.aboutus_view),


    path('adminclick', views.adminclick_view),
    path('doctorclick', views.doctorclick_view),
    path('patientclick', views.patientclick_view),
    path('assistantclick', views.assistantclick_view),

    path('adminsignup', views.admin_signup_view),
    path('doctorsignup', views.doctor_signup_view,name='doctorsignup'),
    path('patientsignup', views.patient_signup_view),
    path('assistantsignup', views.assistant_signup_view,name='assistantsignup'),
    

    # Loginview permet de verifier l'authentification et la validite di formulaire et en cas de success
    # redirige l'utilisateur sur la page spécifié dans la variable LOGIN_REDIRECT_URL='/afterlogin' dans seettings

    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='docteur/doctorlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='patient/patientlogin.html')),
    path('assistantlogin', LoginView.as_view(template_name='assistant/assistantlogin.html')),


    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='home/index.html'),name='logout'),
]

#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('doctor/dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('doctor/agenda', views.doctor_agenda_view,name='doctor-agenda'),
    path('doctor/add_rv', views.add_rv_view,name='doctor-add-rv'),
    path('doctor/delete_rv/<int:idRV>', views.doctor_delete_rv_view,name='doctor-delete-rv'),
    path('doctor/dossier_patients', views.doctor_dossier_patients_view,name='doctor-dossier'),
    path('doctor/dossier_patients/<str:num>', views.doctor_details_patient_view,name='doctor-details-patient'),
    path('doctor/prescription', views.doctor_prescription_view,name='doctor-prescription'),
    path('doctor/patients', views.doctor_patient_view,name='doctor-patient'),
    path('doctor/add_prescription', views.doctor_add_prescription_view,name='doctor-add-prescription')
]

    
    
    
    
#     path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
#     path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
#     path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
#     path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
#     path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
#     path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
#     path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
#     path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),
#     path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),


#     path('admin-assistant', views.admin_assistant_view,name='admin-assistant'),
#     path('admin-view-assistant', views.admin_view_assistant_view,name='admin-view-assistant'),
#     path('delete-assistant-from-hospital/<int:pk>', views.delete_assistant_from_hospital_view,name='delete-assistant-from-hospital'),
#     path('update-assistant/<int:pk>', views.update_assistant_view,name='update-assistant'),
#     path('admin-add-assistant', views.admin_add_assistant_view,name='admin-add-assistant'),
#     path('admin-approve-assistant', views.admin_approve_assistant_view,name='admin-approve-assistant'),
#     path('approve-assistant/<int:pk>', views.approve_assistant_view,name='approve-assistant'),
#     path('reject-assistant/<int:pk>', views.reject_assistant_view,name='reject-assistant'),
   

#     path('admin-patient', views.admin_patient_view,name='admin-patient'),
#     path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
#     path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
#     path('update-patient/<int:pk>', views.update_patient_view,name='update-patient'),
#     path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
#     path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
#     path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
#     path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
#     path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
#     path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
#     path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


#     path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
#     path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
#     path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
#     path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
#     path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
#     path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
# ]




#---------FOR assistant RELATED URLS-------------------------------------
urlpatterns +=[
    path('assistant-dashboard', views.assistant_dashboard_view,name='assistant-dashboard'),

    path('assistant-patient', views.assistant_patient_view,name='assistant-patient'),
    path('assistant-view-patient', views.assistant_view_patient_view,name='assistant-view-patient'),
    path('assistant-view-discharge-patient',views.assistant_view_discharge_patient_view,name='assistant-view-discharge-patient'),

    path('assistant-appointment', views.assistant_appointment_view,name='assistant-appointment'),
    path('assistant-view-appointment', views.assistant_view_appointment_view,name='assistant-view-appointment'),
    path('assistant-delete-appointment',views.assistant_delete_appointment_view,name='assistant-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
]



#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),

]


