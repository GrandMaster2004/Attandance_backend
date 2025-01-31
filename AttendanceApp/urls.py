"""
URL configuration for Attendance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from AttendanceApp.views import signup_view,login_view,user_get_data,superUser_view,superUser_next,profileView,sendEmailotp,isEmailUpdate,sendData
# from AttendanceApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('sign/', signup_view.as_view(), name='signup_view'),
    path('login/', login_view.as_view(), name='login_view'),
    path('saveUserData/', user_get_data.as_view(), name='saveUserData'),
    path('profile/', profileView.as_view(), name='profile_view'),
    path('superUser/', superUser_view.as_view(), name='superUser'),
    path('superUser_next/', superUser_next.as_view(), name='superUsernext'),
    path('sendemail/', sendEmailotp.as_view(), name='sendemail'),
    path('is_email/', isEmailUpdate.as_view(), name='is_email'),
    path('senddata/', sendData.as_view(), name='senddata'),
]
# +static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

# http://127.0.0.1:8000/api/user/login/

