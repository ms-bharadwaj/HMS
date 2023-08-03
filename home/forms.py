from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django import forms
from django.forms import DateTimeInput
class DoctorForm(ModelForm):
    class Meta():
        model= Patient
        fields=['address','mobile','dob']
        
class AccountantForm(ModelForm):
    class Meta():
        model= Accountant
        fields=['address','mobile','dob']
        
class PatientForm(ModelForm):
    
    class Meta():
        model= Patient
        fields=['address','mobile','dob','blood_group']
        
class UserForm(ModelForm):
    class Meta():
     model=User
     fields=['first_name','last_name','email']
     
class AppointmentForm(ModelForm):
    #doctorId=forms.ModelChoiceField(queryset=Doctor.objects.all().filter(available=True),empty_label="Doctor Name and Department")
    class Meta():
        model=Appointment
        fields='__all__'
        widgets = {
            'app_date': forms.widgets.DateTimeInput(),
            'app_time': forms.TimeInput(),
        }
        
        
class PrescriptionForm(ModelForm):
    
    class Meta():
        model=Prescription
        fields=['presc']
        
class InvoiceForm(ModelForm):
    
    class Meta():
        model=Invoice
        fields=['amount']