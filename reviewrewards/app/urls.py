"""reviewrewards URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='index'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('register',views.register,name='register'),
    path('register-action',views.register_action,name='register_action'),
    path('login-action',views.login_action,name='login_action'),
    path('otp-action',views.otp_action,name='otp_action'),
    path('request-verification',views.request_verification,name='request_verification'),
    path('get-available-emails',views.get_available_email,name='get_available_email'),
    path('submit-rate-request',views.submit_rate_request,name='submit_rate_request'),
    path('job',views.job,name='job'),
    path('report',views.report,name='report'),
    path('mark-as-paid',views.mark_as_paid,name='mark_as_paid'),
    path('logout',views.logout,name='logout'),
]
