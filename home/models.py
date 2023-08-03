from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Patient(models.Model):
     user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=False)
     address = models.CharField(max_length=40)
     mobile = models.CharField(max_length=10,null=True)
     dob = models.DateField(max_length=8,default=None,null=True,blank=False)
     age = models.PositiveIntegerField(null=True,blank=True) 
     blood_group=models.CharField(max_length=3,null=True)
     weight=models.PositiveIntegerField(null=True,blank=True) 
     health_conditions=models.TextField(null=True,blank=True)
     @property
     def get_age(self):
          if(self.dob):
               return(datetime.date.today().year-self.dob.year)   
          else:
              return(" ")
     @property
     def full_name(self):
          return(self.user.first_name+' '+self.user.last_name )
     @property
     def pat_id(self):
        return self.user.id
   
   
class Doctor(models.Model):
     user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=False)
     address = models.CharField(max_length=40)
     mobile = models.CharField(max_length=20,null=True)
     dob = models.DateField(max_length=8,null=True,default=None)
     age = models.PositiveIntegerField(null=True,blank=True) 
     department=models.CharField(max_length=20,null=True,blank=True)
     available=models.BooleanField(default=True)
     @property
     def get_age(self):
          if(self.dob):
               return(datetime.date.today().year-self.dob.year) 
          else:
              return(" ")  
     @property
     def full_name(self):
          return(self.user.first_name+' '+self.user.last_name )
     @property
     def doc_id(self):
        return self.user.id
     def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)

class Accountant(models.Model):
     user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=False)
     mobile = models.CharField(max_length=10,null=True)
     address = models.CharField(max_length=40,null=True)
     dob = models.DateField(max_length=8,null=True,default=None)
     def __str__(self):
          return (self.user.first_name)
     
     @property
     def full_name(self):
          return(self.user.first_name+' '+self.user.last_name )
    
     @property
     def acc_id(self):
        return self.user.id
   
     def get_age(self):
          if(self.dob):
               return(datetime.date.today().year-self.dob.year) 
          else:
              return(" ")  
   
   
class Appointment(models.Model):
     created_on=models.DateField(auto_now=True)
     app_date=models.DateField(null=True,blank=True)
     app_time=models.TimeField(null=True,blank=True)
     
     patient=models.ForeignKey(Patient,on_delete=models.SET_NULL,null=True,blank=True)
     doctor=models.ForeignKey(Doctor,on_delete=models.SET_NULL,null=True,blank=True)
          
     patientName=models.CharField(max_length=20,null=True,blank=True)
     doctorName=models.CharField(max_length=40,null=True,blank=True)

     patientId=models.PositiveIntegerField(null=True,blank=True)
     doctorId=models.PositiveIntegerField(null=True,blank=True)
     symptoms=models.TextField(max_length=100,null=True,blank=True)
     status=models.BooleanField(default=False,null=True,blank=True)
     pstatus=models.BooleanField(default=False,null=True,blank=True)
     istatus=models.BooleanField(default=False,null=True,blank=True)

class Prescription(models.Model):
     created_on=models.DateField(auto_now=True,null=True,blank=False)
     appointment=models.OneToOneField(Appointment,on_delete=models.CASCADE)
     presc=models.TextField(max_length=300,null=True)
     status=models.BooleanField(default=False,null=True,blank=True)
     
     
class Invoice(models.Model):
     created_on=models.DateField(auto_now=True,null=True,blank=False)
     appointment=models.OneToOneField(Appointment,on_delete=models.SET_NULL,null=True,blank=True)  
     amount=models.FloatField(max_length=20,null=True,blank=True)
     status=models.BooleanField(default=False,null=True,blank=True)
     created_by=models.ForeignKey(Accountant,on_delete=models.SET_NULL,null=True,blank=False)
     description=models.TextField(max_length=300,null=True)