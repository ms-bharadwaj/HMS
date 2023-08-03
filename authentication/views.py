from django.shortcuts import render

# Create your views here
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .decorators import *
from django.contrib.auth.decorators import login_required
from .decorators import *
from .forms import *
from django.contrib.auth.models import Group
import smtplib
import textwrap

@unauthenticated_user
def loginUser(request):

      if request.method=='POST':
         username=request.POST.get('username') #name in input tag
         password=request.POST.get('password')
         
         user=authenticate(request, username=username, password=password)
         if user is not None:
            login(request,user)
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if(group =='patient'):
                 return redirect ('/hms/patient/pdashboard') 
            elif(group=='doctor') :
                 return redirect ('/hms/doctor/ddashboard') 
            elif(group=='accountant') :
                 return redirect ('/hms/accountant/adashboard') 
            else:
               return redirect('/hms/home')  
            
            return redirect('/hms')
         else:
            messages.info(request,"Username or Password Incorrect")
            return render(request,'login.html')
         
      context={}
      return render(request,'login.html',context)
  
  
@unauthenticated_user
def register(request):
   
   form=CreateUserForm()
   if (request.method=="POST"):
         form=CreateUserForm(request.POST)
         if form.is_valid():
            user=form.save()
            username =form.cleaned_data.get('username')
            group=Group.objects.get(name='patient')
            user.groups.add(group)
            messages.success(request,'Account Created Succesfully for '+username)
            try:
               server= smtplib.SMTP('smtp-mail.outlook.com',587)
               server.starttls()
               content='Greetings from abc clinic!!'
               content=content+'''
               Hello '''+user.first_name
               content=content+'''
               Welcome to world's leading Clinic.
               You have succesfully registered with us.
               We look forward to serving you.'''
               content = textwrap.dedent(content)
               message = 'Subject: {}\n\n{}'.format("ABC Clinic", content)
               server.login('dbms.hms.abc@outlook.com','Hello@hms123')
               server.sendmail('dbms.hms.abc@outlook.com',user.email,message)
            except:
               print("Email not sent")
            return redirect('login')

   
   context={'form':form}
   return render(request,'register.html',context)  

def logoutUser(request):
   logout(request)
   return redirect('login') 