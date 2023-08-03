from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('patient/pdashboard/',views.pdashboard,name='pdash'),
    path('doctor/ddashboard/',views.ddashboard,name='ddash'),
    path('accountant/adashboard/',views.adashboard,name='adash'),
    path('patient/paccountdetails/',views.pInfoPage,name='pinfo'),
    path('doctor/daccountdetails/',views.dInfoPage,name='dinfo'),
    path('patient/editPDetails/<str:pk>',views.editPDetails,name='editP'),
    path('doctor/editDDetails/<str:pk>',views.editDDetails,name='editD'),
    path('doctor/editADetails/<str:pk>',views.editADetails,name='editA'),
    path('patient/bookappointment/<str:pk>',views.bookAppointment,name='book_app'),
    path('patient/upcomingappointments/<str:pk>',views.pUpcomingApp,name='pUpApp'),
    path('patient/pastappointments/<str:pk>',views.pPastApp,name='pPApp'),
    path('doctor/upcomingappointments/<str:pk>',views.dUpcomingApp,name='dUpApp'),
    path('doctor/pastappointments/<str:pk>',views.dPastApp,name='dPApp'),
    path('doctor/manageappointments/<str:pk>',views.dManageApp,name='dMApp'),
    path('doctor/makeprescription/<str:pk>',views.createPrescription,name='dMPresc'),
    path('patient/manageappointments/<str:pk>',views.pManageApp,name='pMApp'),
    path('doctor/deleteappointment/<str:pk>',views.deleteApp,name='delete_app'),
    path('doctor/acceptappointment/<str:pk>',views.acceptApp,name='accept_app'),
    path('doctor/rejectappointment/<str:pk>',views.rejectApp,name='reject_app'),
    path('download_prescription_p/<str:pk>',views.pPrescPdf,name='pDownloadPrescription'),
    path('download_prescription_d/<str:pk>',views.dPrescPdf,name='dDownloadPrescription'),
    path('accountant/generateInvoice/<str:pk>',views.gInvoice,name='gInvoice'),
    path('accountant/pastInvoices/',views.pInvoice,name='pInvoice'),

    path('doctor/stopappointments/<str:pk>',views.stopApp,name='dStopApp'),
    path('doctor/startappointments/<str:pk>',views.startApp,name='dStartApp'),
    path('patient/viewInvoice/<str:pk>',views.view_invoice,name='viewInvoice'),
    
    path('accountant/manageappointments/',views.aManageApp,name='aMApp'),
    path('accountant/upcomingappointments/',views.aUpcomingApp,name='aUpApp'),
    path('patient/aaccountdetails/',views.aInfoPage,name='ainfo'),
]