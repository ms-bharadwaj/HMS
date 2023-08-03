from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect,reverse
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .decorators import *
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group
from .models import *
from . import models
from .forms import *
import datetime
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from unicodedata import normalize
import re
from django.http import JsonResponse
import json
import smtplib
import textwrap


def home(request):
   group=None
   if request.user.groups.exists():
      group=str(request.user.groups.all()[0].name)
   context={'group':group}
   return render(request,'home.html',context)



@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','patient'])
def pdashboard(request):
   try:
      patient = Patient.objects.get(user=request.user)
   except Patient.DoesNotExist:
      patient = Patient.objects.create(user=request.user)
   if(Patient.objects.get(user=request.user)):
      patient=Patient.objects.get(user=request.user)
      patient.save()
      

   
   context={
      'patient':patient,
   }

   return render(request,'pdashboard.html',context)



@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','doctor'])
def ddashboard(request):
   try:
      doctor=Doctor.objects.get(user=request.user)
   except Doctor.DoesNotExist:
      doctor = Doctor.objects.create(user=request.user)
   context={
      'doctor':doctor,
   }
   return render(request,'ddashboard.html',context)







@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','doctor'])
def dInfoPage(request):
   doctor=Doctor.objects.get(user=request.user)
   context={
      'doctor':doctor,
      
   }
   return render(request,'dinfo.html',context)



@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','patient'])
def pInfoPage(request):
   patient=Patient.objects.get(user=request.user)
   context={
      'patient':patient,
      
   }
   return render(request,'pinfo.html',context)

@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','patient'])
def editPDetails(request,pk):
   if(int(pk)==request.user.id):
      user=User.objects.get(id=int(pk))
      userI=User.objects.get(id=user.id)
      patient=Patient.objects.get(user=user)
      pform=PatientForm(instance=patient)
      uform=UserForm(instance=userI)
      if request.method=="POST":
         pform=PatientForm(request.POST,instance=patient)
         uform=UserForm(request.POST,instance=userI)
         if pform.is_valid() and uform.is_valid():
            pform.save()
            uform.save()
            return redirect('/hms/patient/pdashboard')
      context={
         'pform':pform,
         'uform':uform,
      }
      return render(request,'editPatientDetails.html',context)
   else:
      return HttpResponse("Unautherised access")
   
   
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','doctor'])
def editDDetails(request,pk):
   if(int(pk)==request.user.id):
      user=User.objects.get(id=int(pk))
      userI=User.objects.get(id=user.id)
      doctor=Doctor.objects.get(user=user)
      dform=DoctorForm(instance=doctor)
      uform=UserForm(instance=userI)
      if request.method=="POST":
         dform=DoctorForm(request.POST,instance=doctor)
         uform=UserForm(request.POST,instance=userI)
         if dform.is_valid() and uform.is_valid():
            dform.save()
            uform.save()
            return redirect('/hms/doctor/ddashboard')
      context={
         'dform':dform,
         'uform':uform,
      }
      return render(request,'editDoctorDetails.html',context)
   else:
      return HttpResponse("Unautherised access")
   
   
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','accountant'])
def editADetails(request,pk):
   if(int(pk)==request.user.id):
      user=User.objects.get(id=int(pk))
      userI=User.objects.get(id=user.id)
      accountant=Accountant.objects.get(user=user)
      aform=AccountantForm(instance=accountant)
      uform=UserForm(instance=userI)
      if request.method=="POST":
         aform=AccountantForm(request.POST,instance=accountant)
         uform=UserForm(request.POST,instance=userI)
         if aform.is_valid() and uform.is_valid():
            aform.save()
            uform.save()
            return redirect('/hms/accountant/adashboard')
      context={
         'aform':aform,
         'uform':uform,
      }
      return render(request,'editAccountantDetails.html',context)
   else:
      return HttpResponse("Unautherised access")
   
   
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','patient']) 
def bookAppointment(request,pk):
   if(request.user.id==int(pk)):
      form=AppointmentForm()
      user=User.objects.get(id=request.user.id)
      context={
         'form':form,
         'doctors':Doctor.objects.filter(available="True"),
      }
      if(request.method=='POST'):
         appointmentForm=AppointmentForm(request.POST)
         if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            docId=request.POST.get('doctorId')
            # appointment.app_date_time=request.POST.get('app_date_time')
            appointment.app_date=request.POST.get('app_date')
            appointment.app_time=request.POST.get('app_time')
            appointment.patientId=request.user.id
            docUser=User.objects.get(id=docId)
            patUser=User.objects.get(id=request.user.id)
            appointment.doctorName=Doctor.objects.get(user=docUser).full_name
            appointment.doctor=Doctor.objects.get(user=docUser)
            appointment.patient=Patient.objects.get(user=patUser)
            appointment.patientName=Patient.objects.get(user=user).full_name
            appointment.status=False
            app_date_time=request.POST.get('app_date_time')
            cur_date_time=str(datetime.datetime.now())
            appointment.save()
            prescription=Prescription.objects.create(appointment=appointment)
            prescription.save()
            # if(datetime.datetime.strptime(app_date_time,'%y/%m/%d') > datetime.datetime.strptime(cur_date_time,'%y/%m/%d')):
               
            # else:
            #    raise forms.ValidationError("The date cannot be in the past!")
            return redirect('/hms/patient/pdashboard')
         else:
            
            return HttpResponse("Errors in input details please enter correct details")
            
      return render(request,'bookAppointment.html',context)   
   else:
      
      return HttpResponse("Unautherised access")
   
   
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','patient']) 
def pPastApp(request,pk):
   if request.user.id==int(pk):
         appointments=Appointment.objects.filter(status=True,patientId=request.user.id,pstatus=True)
         context={
            'appointments':appointments,
            
            }
         return render(request,"pPastAppointments.html",context) 
   else:
         return HttpResponse("Unauthorised access")
   
   
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','patient']) 
def pUpcomingApp(request,pk):
   if request.user.id==int(pk):
      appointments=Appointment.objects.filter(status=True,patientId=request.user.id,pstatus=False)
      context={
         'appointments':appointments,
         }
      return render(request,"pUpcomingAppointments.html",context)
   else:
      return HttpResponse("Unauthorised access")
   
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','doctor'])    

def dUpcomingApp(request,pk):
    if request.user.id==int(pk):
      appointments=Appointment.objects.filter(status=True,doctorId=request.user.id,pstatus=False)
      context={
         'appointments':appointments,
         
         }
      return render(request,"dUpcomingAppointments.html",context) 
    else:
      return HttpResponse("Unauthorised access")

@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','doctor']) 
def dPastApp(request,pk):
    if request.user.id==int(pk):
      appointments=Appointment.objects.filter(status=True,doctorId=request.user.id,pstatus=True)
      context={
         'appointments':appointments,
         
         }
      return render(request,"dPastAppointments.html",context) 
    else:
      return HttpResponse("Unauthorised access")
   
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','doctor']) 
def dManageApp(request,pk):
    if request.user.id==int(pk):
       appointments=Appointment.objects.filter(doctorId=request.user.id,pstatus=False)
       context={
         'appointments':appointments,
         
         }
       return render(request,"dManageApp.html",context)
    else:
      return HttpResponse("Unauthorised access")
   
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','doctor']) 
def acceptApp(request,pk):
   if(Appointment.objects.get(id=pk,doctorId=request.user.id)):
      appointment=Appointment.objects.get(id=pk)
      appointment.status=True
      appointment.save()
      try:
               user=User.objects.get(id=appointment.patientId)
               server= smtplib.SMTP('smtp-mail.outlook.com',587)
               server.starttls()
               content='Greetings from abc clinic!!'
               content=content+'''
               Hello '''+user.first_name
               content=content+'''
               
               Your appointment with '''+appointment.doctorName+' scheduled on '+ str(appointment.app_date_time)+' is accepted'
               content=content+'''
               
               Please be on time.
               Regards
               ABC Clinic
               '''
               content = textwrap.dedent(content)
               message = 'Subject: {}\n\n{}'.format("ABC Clinic", content)
               server.login('dbms.hms.abc@outlook.com','Hello@hms123')
               server.sendmail('dbms.hms.abc@outlook.com',user.email,message)
               print("Hello")
      except:
               print("Email not sent")
      return redirect('/hms/doctor/ddashboard/')
   else:
      return HttpResponse("Unauthorised access")
 
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','doctor']) 
def rejectApp(request,pk):
      if(Appointment.objects.get(id=pk,doctorId=request.user.id)):
         appointment=Appointment.objects.get(id=pk)
         if(appointment.status== True):
            try:
                  user=User.objects.get(id=appointment.patientId)
                  server= smtplib.SMTP('smtp-mail.outlook.com',587)
                  server.starttls()
                  content='Greetings from ABC clinic!!'
                  content=content+'''
                  Hello '''+user.first_name
                  content=content+'''
                  
                  Your appointment with '''+appointment.doctorName+' scheduled on '+ str(appointment.app_date_time)+' was cancelled'
                  content=content+'''
                  
                  Sorry for the inconvinience.
                  Regards
                  ABC Clinic
                  '''
                  content = textwrap.dedent(content)
                  message = 'Subject: {}\n\n{}'.format("ABC Clinic", content)
                  server.login('dbms.hms.abc@outlook.com','Hello@hms123')
                  server.sendmail('dbms.hms.abc@outlook.com',user.email,message)
                  print("Hello")
            except:
                  print("Email not sent")
         appointment.delete()
         return redirect('/hms/doctor/ddashboard/')
      else:
         return HttpResponse("Unauthorised access")


   
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','patient']) 
def pManageApp(request,pk):
    if request.user.id==int(pk):
       appointments=Appointment.objects.filter(patientId=request.user.id,pstatus=False)
       context={
         'appointments':appointments,
         
         }
       return render(request,"pManageApp.html",context)
    else:
      return HttpResponse("Unauthorised access")
   
   
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','patient']) 
def deleteApp(request,pk):
      if(Appointment.objects.get(id=pk,patientId=request.user.id)):
         appointment=Appointment.objects.get(id=pk)
         appointment.delete()
         return redirect('/hms/patient/manageappointments/'+str(request.user.id))
      else:
         return HttpResponse("Unauthorised access") 
      
      
      
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','doctor']) 
def createPrescription(request,pk):
   if(Appointment.objects.get(id=int(pk),doctorId=request.user.id,pstatus=False)):
      appointment=Appointment.objects.get(id=int(pk))
      if(not Prescription.objects.get(appointment=appointment)):
         prescription=Prescription.objects.create(appointment=appointment)
         prescription.save()
      prescription= Prescription.objects.get(appointment=appointment)
      form=PrescriptionForm(instance=prescription);   
      context={
         'form':form,
         'appointment':appointment,
      }
      
      if request.method=="POST":
            form=PrescriptionForm(request.POST,instance=prescription);
            if form.is_valid():
               presc=form.save(commit=False)
               presc.status=True
               presc.save()
               appointment.pstatus=True
               appointment.save()
               return redirect('/hms/doctor/manageappointments/'+str(request.user.id))
            
            else:
               return HttpResponse("Invalid Form Input") 
            
            
      return render(request,'makePrescription.html',context)      
   else:
      return HttpResponse("Unauthorised access") 
      
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','patient'])      
def pPrescPdf(request,pk): 
  
   if(Appointment.objects.get(patientId=request.user.id,id=int(pk))):  
         appointment=Appointment.objects.get(id=int(pk))
         prescription=Prescription.objects.get(appointment=appointment)
         context={
         'appointment':appointment,
         'prescription':prescription,
         'list':(prescription.presc).splitlines()
         }
         return render(request,'Prescription.html',context)
         # buf=io.BytesIO()
         # c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
         

         
         # lines=[]  
         # lines.append("                                ABCD Diagnostic Centre                           ")
         # lines.append("                                                   K Circle                              ")    
         # lines.append('')
         # lines.append("Consulting Doctor: "+appointment.doctorName)
         # lines.append('------------------------------------------------------------------------------------------------------')
         # lines.append("Patient Name: "+appointment.patientName) 
         # lines.append("Consultation Date: "+str(((appointment.app_date)) ))
         # lines.append('')
         # lines.append('')
         # lines.append('Rx')
         # lines.append('')
         # lines.append(prescription.presc)
         # lines.append('')
         # lines.append('')
         # lines.append('------------------------------------------------------------------------------------------------------')
         
         
         
         # buf=io.BytesIO()
         # c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
         
         # textob= c.beginText()
         # textob.setTextOrigin(inch,inch)
         # font="Helvetica"
         # size=15
         # textob.setFont(font,size)
         # c.drawImage("C:/Users/manis/Desktop/HMS - Copy (2)/hms/home/static/logonew.jpg", x=120, y=40, width=70, height=60)
         # cnt=0
         # for line in lines:
         #    if cnt==0 or cnt==9:
         #       textob.setFont(font,17)
         #    else:
         #       textob.setFont(font,size)
         #    cnt=cnt+1
         #    textob.textLine(line)
            
         
         # c.drawText(textob)
         # c.showPage()
         # c.save()
         # buf.seek(0)
         # return FileResponse(buf,as_attachment=True,filename=appointment.patientName+'.pdf')
   else:
      return HttpResponse("Unauthorised access") 
      
   
   
   
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','doctor'])    
def dPrescPdf(request,pk): 
   
   if(Appointment.objects.get(doctorId=request.user.id,id=int(pk))):  
      appointment=Appointment.objects.get(id=pk)
      prescription=Prescription.objects.get(appointment=appointment)
      context={
         'appointment':appointment,
        'prescription':prescription
      }
      return render(request,'Prescription.html',context)
      
      # buf=io.BytesIO()
      # c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
      

      
      # lines=[]  
      # lines.append("                                ABCD Diagnostic Centre                           ")
      # lines.append("                                                   K Circle                              ")    
      # lines.append('')
      # lines.append("Consulting Doctor: "+appointment.doctorName)
      # lines.append('------------------------------------------------------------------------------------------------------')
      # lines.append("Patient Name: "+appointment.patientName) 
      # lines.append("Consultation Date: "+str(((appointment.app_date_time).date()).strftime("%d %B %Y")) )
      # lines.append('')
      # lines.append('')
      # lines.append('Rx')
      # lines.append('')
      # text=prescription.presc
      # lines.append(text)
      # lines.append('')
      # lines.append('')
      # lines.append('------------------------------------------------------------------------------------------------------')
      
      
      
      # buf=io.BytesIO()
      # c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
      
      # textob= c.beginText()
      # textob.setTextOrigin(inch,inch)
      # font="Helvetica"
      # size=15
      # textob.setFont(font,size)
      # c.drawImage("C:/Users/manis/Desktop/HMS/hms/home/templates/logo.jpg", x=120, y=40, width=70, height=60)
      # cnt=0
      # for line in lines:
      #    if cnt==0 or cnt==9:
      #       textob.setFont(font,17)
      #    else:
      #       textob.setFont(font,size)
      #    cnt=cnt+1
      #    textob.textLine(line)
         
      
      # c.drawText(textob)
      # c.showPage()
      # c.save()
      # buf.seek(0)
      # return FileResponse(buf,as_attachment=True,filename=appointment.patientName+'.pdf')
   else:
      return HttpResponse("Unauthorised access") 

   
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','doctor'])    
def stopApp(request,pk):
   if(request.user.id==int(pk)):
      user=User.objects.get(id=int(pk))
      doctor=Doctor.objects.get(user=user)
      doctor.available=False
      doctor.save()
      print(str(doctor.available))
      return redirect('/hms/doctor/ddashboard/')
   else:
      return HttpResponse("Unauthorised access") 

   
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','doctor'])    
def startApp(request,pk):
   if(request.user.id==int(pk)):
      user=User.objects.get(id=int(pk))
      doctor=Doctor.objects.get(user=user)
      doctor.available=True
      doctor.save()
      return redirect('/hms/doctor/ddashboard/')
   else:
      return HttpResponse("Unauthorised access") 


@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','accountant'])
def adashboard(request):
   try:
      accountant=Accountant.objects.get(user=request.user)
   except Accountant.DoesNotExist:
      accountant = Accountant.objects.create(user=request.user)
      
   appointments=Appointment.objects.filter(pstatus=True,istatus=False)
   context={
      'accountant':accountant,
      'appointments':appointments,
   }
   return render(request,'adashboard.html',context)



@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','accountant'])
def gInvoice(request,pk):
   if(Appointment.objects.get(id=int(pk),istatus=False)):
      appointment=Appointment.objects.get(id=int(pk))
      if(not Invoice.objects.filter(appointment=appointment)):
         print("Good")
         invoice=Invoice.objects.create(appointment=appointment)
         invoice.save()
      invoice= Invoice.objects.get(appointment=appointment)
      # form=InvoiceForm(instance=invoice);   
      # context={
      #    'form':form,
      #    'invoice':invoice,
      # }
      
   if request.method=="POST":
         # form=InvoiceForm(request.POST,instance=invoice);
         # if form.is_valid():
         #    invo=form.save(commit=False)
         #    accountant=Accountant.objects.get(user=request.user)
         #    invo.created_by=accountant
         #    invo.status=True
         #    invo.save()
         #    appointment.istatus=True
         #    appointment.save()
         #    return redirect('/hms/accountant/adashboard/')
         
            # else:
            #    return HttpResponse("Invalid Form Input") 
      description = request.POST.get('description')
      total_amount =float(request.POST.get('total_amount'))
      invoice.description=description
      invoice.amount=total_amount
      # Invoice.objects.create(description=description,amount=total_amount)
      accountant=Accountant.objects.get(user=request.user)
      invoice.created_by=accountant
      invoice.status=True
      invoice.save()
      appointment.istatus=True
      appointment.save()
      return redirect('/hms/accountant/adashboard/')
      
   return render(request,'generateInvoice.html')      
 
#past invoice
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','accountant'])
def pInvoice(request):
   queryset = Invoice.objects.filter(status=True).select_related('appointment').values('amount',  'created_by', 'created_on','appointment__app_date','appointment__app_time','appointment__patientName','appointment__doctorName')
   
   context={
         'queryset':queryset,
        
      }
   return render(request,'pInvoices.html',context)

@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','patient'])
def view_invoice(request,pk):
   if(Appointment.objects.get(id=pk,patientId=request.user.id)):
      appointment=Appointment.objects.get(id=pk)
      invoice=Invoice.objects.get(appointment=appointment)
      context={
         "invoice":invoice,
          'appointment':appointment,
      }
      return render(request,'viewInvoice.html',context)
   else:
      return HttpResponse("Unauthorised Access")
   
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','accountant'])   
def aManageApp(request):
   appointments=Appointment.objects.filter(pstatus=True,istatus=False)
   context={
      
      'appointments':appointments,
   }
   return render(request,'aManageApp.html',context)
 
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','accountant'])   
def aUpcomingApp(request):
   appointments=Appointment.objects.filter(pstatus=False,istatus=False)
   context={
      
      'appointments':appointments,
   }
   return render(request,'aUpcomingApp.html',context)
 
@login_required(login_url='login') 
@allowed_users(allowed_roles=['admin','accountant'])          
def aInfoPage(request):
   accountant=Accountant.objects.get(user=request.user)
   context={
      'accountant':accountant,
      
   }
   return render(request,'ainfo.html',context)