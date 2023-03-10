from django.shortcuts import render,redirect,reverse
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.utils import timezone


from . import forms,models

# Create your views here.
def home_view(request):
    return render(request,'home/index.html')


#for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')


#for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    if(request.user.is_authenticated):
        return HttpResponseRedirect('afterlogin')
    return render(request,'docteur/doctorclick.html')

#for showing signup/login button for assistant(by sumit)
def assistantclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'assistant/assistantclick.html')


#for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'patient/patientclick.html')

def interface_docteur(request):
    return render(request,'docteur/dashbord.html')



def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})




def doctor_signup_view(request):
    userForm=forms.UserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.UserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTEUR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'docteur/doctorsignup.html',context=mydict)

def assistant_signup_view(request):
    userForm=forms.UserForm()
    AssistantForm=forms.AssistantForm()
    mydict={'userForm':userForm,'assistantForm':AssistantForm}
    if request.method=='POST':
        userForm=forms.UserForm(request.POST)
        AssistantForm=forms.AssistantForm(request.POST,request.FILES)
        if userForm.is_valid() and AssistantForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            assistant=AssistantForm.save(commit=False)
            assistant.user=user
            assistant=assistant.save()
            my_assistant_group = Group.objects.get_or_create(name='SECRETAIRE')
            my_assistant_group[0].user_set.add(user)
        return HttpResponseRedirect('assistantlogin')
    return render(request,'assistant/assistantsignup.html',context=mydict)


def patient_signup_view(request):
    userForm=forms.UserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            #patient.secretaire =request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'patient/patientsignup.html',context=mydict)






#-----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTEUR').exists()
def is_assistant(user):
    return user.groups.filter(name='SECRETAIRE').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        docteur = models.Docteur.objects.filter(user_id=request.user.id).get()
        docteur = docteur.get_full_name()
        accountapproval=models.Docteur.objects.all().filter(status=True,user_id=request.user.id)
        if accountapproval:
            return redirect('doctor/dashboard')
        else:
            return render(request,'docteur/doctor_wait_for_approval.html',context={'docteur':docteur})
    elif is_assistant(request.user):
        accountapproval=models.Secretaire.objects.all().filter(status=True,user_id=request.user.id)
        if accountapproval:
            return redirect('assistant-dashboard')
        else:
            return render(request,'hospital/assistant_wait_for_approval.html')    
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(status=True, user_id=request.user.id)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'hospital/patient_wait_for_approval.html')
    return HttpResponseRedirect()


#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED ROLE VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def add_rv_view(request):
    rvForm = forms.Rendez_vousForm(request.POST)
    docteur = models.Docteur.objects.filter(user_id=request.user.id).get()
    if rvForm.is_valid():
        print(request.POST)
        rvForm.cleaned_data['docteur']=models.Docteur.objects.filter(user_id=request.user.id).get()
        rv = rvForm.save()
        return redirect('doctor-agenda')
    return render(request,'docteur/addRV.html',context={'rvForm':rvForm})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_rv_view(request,idRV):
    if request.method=='GET':
        rv = models.RendezVous.objects.filter(id=idRV)
        rv.delete()
        return redirect('doctor-agenda')
    return render(request,'docteur/agenda.html')







#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_specialisation.html',{'doctors':doctors})


def admin_assistant_view(request):
    return render(request,'hospital/admin_assistant.html')

def admin_view_assistant_view(request):
    assistants=models.assistant.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_assistant.html',{'assistants':assistants})

def delete_assistant_from_hospital_view(request,pk):
    assistant=models.assistant.objects.get(id=pk)
    user=models.User.objects.get(id=assistant.user_id)
    assistant.delete()
    return redirect('admin-view-assistant')

def update_assistant_view(request,pk):
    assistant=models.assistant.objects.get(id=pk)
    user=models.User.objects.get(id=assistant.user_id)
    userForm=forms.assistantUserForm(instance=user)
    assistantForm=forms.assistantForm(request.FILES,instance=assistant)
    mydict={'userForm':userForm,'assistantForm':assistantForm}
    userForm=forms.assistantUserForm(request.POST,instance=user)
    assistantForm=forms.assistantForm(request.POST,request.FILES,instance=assistant)
    if userForm.is_valid() and assistantForm.is_valid():
            assistant=assistantForm.save(commit=False)
            assistant.status=True
            assistant.save()
            return redirect('admin-view-assistant')
    return render(request,'hospital/admin_update_assistant.html',context=mydict)

def admin_add_assistant_view(request):
    userForm=forms.assistantUserForm()
    assistantForm=forms.assistantForm()
    mydict={'userForm':userForm,'assistantForm':assistantForm}
    userForm=forms.assistantUserForm(request.POST)
    assistantForm=forms.assistantForm(request.POST, request.FILES)
    if userForm.is_valid() and assistantForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            my_assistant_group = Group.objects.get_or_create(name='assistant')
            my_assistant_group[0].user_set.add(user)
            return HttpResponseRedirect('admin-view-assistant')
    return render(request,'hospital/admin_add_assistant.html',context=mydict)

def admin_approve_assistant_view(request):
    assistants=models.assistant.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_assistant.html',{'assistants':assistants})

def approve_assistant_view(request,pk):
    assistant=models.assistant.objects.get(id=pk)
    assistant.status=True
    assistant.save()
    return redirect(reverse('admin-approve-assistant'))

def reject_assistant_view(request,pk):
    assistant=models.assistant.objects.get(id=pk)
    user=models.User.objects.get(id=assistant.user_id)
    assistant.delete()
    return redirect('admin-approve-assistant')

def admin_view_assistant_specialisation_view(request):
    assistants=models.assistant.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_assistant_specialisation.html',{'assistants':assistants})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'hospital/admin_patient.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'hospital/admin_update_patient.html',context=mydict)





@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status=True
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'hospital/admin_add_patient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'hospital/admin_discharge_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':
        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'hospital/patient_final_bill.html',context=patientDict)
    return render(request,'hospital/patient_generate_bill.html',context=patientDict)



#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'hospital/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'hospital/admin_add_appointment.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
def doctor_dashboard_view(request):

    docteur = models.Docteur.objects.filter(user_id=request.user.id).get()

    today = datetime.now().date()
    today_appointments = models.RendezVous.objects.filter(docteur=docteur, date=today).all()
    all_appointments = models.RendezVous.objects.filter(docteur=docteur).order_by('date')
    tomorrow = today + timedelta(days=1)
    future_appointments = models.RendezVous.objects.filter(docteur=docteur, date__gte=tomorrow).all()
    rdv_today = today_appointments.count()
    next_rdv = future_appointments.count()

    patients_service = models.Patient.objects.filter(services=docteur.service)

    # R??cup??ration des patients li??s aux rendez-vous du docteur connect??
    patients_appointments = models.Patient.objects.filter(rendez_vous_patient__docteur=docteur)

    # R??cup??ration des patients li??s au service du docteur connect?? et aux rendez-vous du docteur connect??
    patients = patients_service | patients_appointments

    # Suppression des duplicatas
    patients = patients.distinct()
    patient_count = patients.distinct().count()
   
    data = {
    'today_appointments': today_appointments,
    'patients': patients,
    'docteur': docteur,
    'patient_count': patient_count,
    'future_appointments':future_appointments,
    'all_appointments': all_appointments,
    'rdv_today':rdv_today,
    'next_rdv':next_rdv
    }
    return render(request,'docteur/dashboard.html',context=data)



# @login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    docteur = models.Docteur.objects.filter(user_id=request.user.id).get()
    patients_service = models.Patient.objects.filter(services=docteur.service)
    # R??cup??ration des patients li??s aux rendez-vous du docteur connect??
    patients_appointments = models.Patient.objects.filter(rendez_vous_patient__docteur=docteur)
    # R??cup??ration des patients li??s au service du docteur connect?? et aux rendez-vous du docteur connect??
    patients = patients_service | patients_appointments
    # Suppression des duplicatas
    patients = patients.distinct().order_by('admission')
    patient_count = patients.distinct().count()
    data={'patients':patients ,'nb_patient':patient_count,'docteur':docteur}
    return render(request,'docteur/patients.html',context=data)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_agenda_view(request):
    docteur = models.Docteur.objects.filter(user_id=request.user.id).get()
    today = datetime.now().date()
    today_appointments = models.RendezVous.objects.filter(docteur=docteur, date=today).all()
    tomorrow = today + timedelta(days=1)
    future_appointments = models.RendezVous.objects.filter(docteur=docteur, date__gte=tomorrow).all()
    past_appointments = models.RendezVous.objects.filter(docteur=docteur, date__lt=today).all()
    rdv_today = today_appointments.count()
    next_rdv = future_appointments.count()
    past_rdv = past_appointments.count()
    
    #----------------Ajout RV-------------------#
    form = False
    patients_service = models.Patient.objects.filter(services=docteur.service)
    # R??cup??ration des patients li??s aux rendez-vous du docteur connect??
    patients_appointments = models.Patient.objects.filter(rendez_vous_patient__docteur=docteur)
    # R??cup??ration des patients li??s au service du docteur connect?? et aux rendez-vous du docteur connect??
    patients = patients_service | patients_appointments
    # Suppression des duplicatas
    patients = patients.distinct()
    if request.method == 'GET':
        form = True 
    rvForm=forms.Rendez_vousForm(initial={'docteur': docteur.get_full_name()})
    rvForm.fields['patients'].queryset = patients.order_by('prenom')
    data = {
    'rvForm':rvForm,
    'form':form,
    'docteur': docteur,
    'today_appointments':today_appointments,
    'rdv_today': rdv_today,
    'future_appointments':future_appointments,
    'next_rdv':next_rdv,
    'past_appointments':past_appointments,
    'past_rdv':past_rdv
    }
    return render(request,'docteur/agenda.html',context=data)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dossier_patients_view(request):
    docteur = models.Docteur.objects.filter(user_id=request.user.id).get()
    dossiers = models.DossierMedical.objects.filter(service=docteur.service).all()
    dossier_count = models.DossierMedical.objects.filter(service=docteur.service).all().count()
    data ={'docteur':docteur, 'dossiers':dossiers,'nb_dossier':dossier_count}
    return render(request,'docteur/dossierpatients.html',context=data)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)   
def doctor_details_patient_view(request,num):
    dossier = models.DossierMedical.objects.filter(numero=num).get()
    patient = models.Patient.objects.filter(id=dossier.patient.id).get()
    ordonnances = models.Ordonnance.objects.filter(dossier_medical=dossier.id)
    rendezVous = models.RendezVous.objects.filter(patients=patient)
    mydata={'dossier':dossier,'ordonnances':ordonnances,'patient':patient,'rendezVous':rendezVous }
    return render(request,'docteur/detailpatient.html',context=mydata)

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_prescription_view(request):
    docteur = models.Docteur.objects.filter(user_id=request.user.id).get()
    ordonnances = models.Ordonnance.objects.filter(docteur=docteur).all()
    ordonnance_count = models.Ordonnance.objects.filter(docteur=docteur).all().count()
    data ={'docteur':docteur, 'ordonnances':ordonnances,'nb_ordonnance':ordonnance_count}
    return render(request,'docteur/prescription.html',context=data)


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_add_prescription_view(request):
    ordonnanceForm = forms.OrdonnanceForm()
    docteur = models.Docteur.objects.filter(user_id=request.user.id).get()
    ordonnanceForm=forms.OrdonnanceForm(initial={'docteur': docteur})
    print(docteur)
    if request.method == 'POST':
        ordonnanceForm = forms.OrdonnanceForm(request.POST)
        if ordonnanceForm.is_valid():
            ordonnanceForm.cleaned_data['docteur'] = docteur
            ordonnanceForm.save()
        return HttpResponseRedirect('prescription')
    return render(request,'docteur/addprescription.html',context={'ordonnanceForm':ordonnanceForm})


# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



# @login_required(login_url='doctorlogin')
# @user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------



#------------------------ assistant RELATED VIEWS START ------------------------------
# @login_required(login_url='assistantlogin')
# @user_passes_test(is_assistant)
def assistant_dashboard_view(request):
    assistant =models.Secretaire.objects.get(user_id=request.user.id)
    patientcount=models.Patient.objects.all().filter(secretaire_id=assistant.id).count()
    patients=models.Patient.objects.all().filter(secretaire_id=assistant.id)
    patients = list(patients)
    appointment_assistant=0
    for patient in patients:
        if(models.RendezVous.objects.all().filter(patients_id=patient.id).exists()):
            appointment_assistant+=1
   
    #for  table in assistant dashboard
    appointments=models.RendezVous.objects.all().order_by('date')
    return render(request,'assistant/assistant_dashboard.html',{'assistant':assistant,'rv':appointments,'patients':patients})
    

def assistant_patient_view(request):
    pass

@login_required(login_url='assistantlogin')
@user_passes_test(is_assistant)
def assistant_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedassistantId=request.user.id)
    assistant=models.Assistant.objects.get(user_id=request.user.id) #for profile picture of assistant in sidebar
    return render(request,'hospital/assistant_view_patient.html',{'patients':patients,'assistant':assistant})

@login_required(login_url='assistantlogin')
@user_passes_test(is_assistant)
def assistant_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedassistantName=request.user.first_name)
    assistant=models.Assistant.objects.get(user_id=request.user.id) #for profile picture of assistant in sidebar
    return render(request,'hospital/assistant_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'assistant':assistant})

@login_required(login_url='assistantlogin')
@user_passes_test(is_assistant)
def assistant_appointment_view(request):
    assistant=models.Assistant.objects.get(user_id=request.user.id) #for profile picture of assistant in sidebar
    return render(request,'hospital/assistant_appointment.html',{'assistant':assistant})

@login_required(login_url='assistantlogin')
@user_passes_test(is_assistant)
def assistant_view_appointment_view(request):
    assistant=models.Assistant.objects.get(user_id=request.user.id) #for profile picture of assistant in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,assistantId=request.user.id)
    return render(request,'hospital/assistant_view_appointment.html',{'appointments':appointments,'assistant':assistant})

@login_required(login_url='assistantlogin')
@user_passes_test(is_assistant)
def assistant_delete_appointment_view(request):
    assistant=models.Assistant.objects.get(user_id=request.user.id) #for profile picture of assistant in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,assistantId=request.user.id)
    return render(request,'hospital/assistant_delete_appointment.html',{'appointments':appointments,'assistant':assistant})

#------------------------ assistant RELATED VIEWS END ------------------------------



#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            if doctor.department == 'Cardiologist':
                if 'heart' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})


            if doctor.department == 'Dermatologists':
                if 'skin' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Emergency Medicine Specialists':
                if 'fever' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Allergists/Immunologists':
                if 'allergy' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Anesthesiologists':
                if 'surgery' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})

            if doctor.department == 'Colon and Rectal Surgeons':
                if 'cancer' in desc:
                    pass
                else:
                    print('else')
                    message="Please Choose Doctor According To Disease"
                    return render(request,'hospital/patient_book_appointment.html',{'appointmentForm':appointmentForm,'patient':patient,'message':message})





            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.assistantId=request.POST.get('assistantId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'hospital/patient_book_appointment.html',context=mydict)





@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'contact/contactussuccess.html')
    return render(request, 'contact/contactus.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------

