from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .form import StudentForm
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import auth
from .models import subOtp
from django.contrib.auth import get_user_model
User = get_user_model()
import random
from django.urls import reverse
import smtplib
from .models import subOtp,cseData,itData,eceData
import pandas as pd
from django.http import JsonResponse
# from geopy.distance import geodesic
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from rest_framework_simplejwt.tokens import RefreshToken
import os
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from AttendanceApp.renderers import UserRenderer
from AttendanceApp.serializers import signup_viewSerializer,UserLoginSerializer,UserDataSerializer,SuperUserDataSerializerfirst,SuperUserDataSerializersecond,SerializeUserData,SerializesendEmail,UpdateIsemail,StudentListSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
import math

# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }


def send_email_with_attachment(receiver_email, subject, content, file_path):
  sender_email = "eurekadigital6@gmail.com"
  password = "yags nldl objv doyv"
  message = MIMEMultipart()
  message["From"] = sender_email
  message["To"] = receiver_email
  message["Subject"] = subject

  # Attach the text content
  message.attach(MIMEText(content, "plain"))
  with open(file_path, "rb") as file:
    message.attach(MIMEApplication(file.read(), Name=file_path))

  server = smtplib.SMTP("smtp.gmail.com", 587)
  server.starttls()
  server.login(sender_email, password)
  server.sendmail(sender_email, receiver_email, message.as_string())
  server.quit()
  os.remove(file_path) #jfdslfjk this file remove


# delete waha pr karna ok buddy
def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in meters
    R = 6371000
    
    # Convert degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    # Haversine formula
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Distance in meters
    distance = R * c
    return distance



def send_otp(email,otp):
    receiver_email = email
    sender_email = "eurekadigital6@gmail.com"
    # print(receiver_email)
    password = "yags nldl objv doyv"
    subject = str(otp)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email,subject)

def send_file(email, data):
    # print(data)
    receiver_email = email
    sender_email = "eurekadigital6@gmail.com"
    password = "yags nldl objv doyv"
    subject = str(data)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email,subject)


class signup_view(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = signup_viewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)
    
    
def profile_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff==False:
            otp = random.randint(1000,9999)
            email = request.user.email
            if(request.POST.get('otp1')==None):
                send_otp(email, otp)
            elif request.method=='POST':
                otp1 = request.POST.get('otp1')
                otp2 = request.POST.get('otp2')
                print(f"{otp1} and {otp2}")
                if(otp1==otp2):
                    request.user.is_staff = True
                    request.user.save()
                else:
                    send_otp(email, otp)
            return render(request, './AttendanceApp/profile.html',{'otp2':otp})
    else:
        # print("some thing wrong")
        return redirect('/logout_view')
    return render(request, './AttendanceApp/profile.html')

class login_view(APIView):
  renderer_classes = [UserRenderer]
  def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        roll_no = serializer.data.get('roll_no')
        password = serializer.data.get('password')
        # print(roll_no, password)
        user = authenticate(roll_no=roll_no, password=password)
        # print(f"hgj gg {user}")
        if user is not None:
            token = get_tokens_for_user(user)
            print(f"{user} jhj hh ")
            # print(f"hgj gg1 {token}")
            return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            # print(f"hgj gg2 {token}")
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)


class user_get_data(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserDataSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        roll_no = serializer.data.get('roll_no')
        branch = serializer.data.get('branch')
        section = serializer.data.get('section')
        name = serializer.data.get('student_name')
        year = serializer.data.get('year')
        code = serializer.data.get('subCode')
        otp = serializer.data.get('otp')
        latitude = serializer.data.get('longitude')
        longitude = serializer.data.get('latitude')
        number = serializer.data.get('number')
        print(serializer)
        # now we need to verify location and otp
        if(branch=="CSE"):
            var = subOtp.objects.all()
            ind = False
            for one in var:
                if(one.otp==otp):
                    coord1 = (one.langitude, one.londitude) # Coordinates of 2
                    coord2 = (latitude, longitude) # Coordinates of 1
                    displacement = haversine(float(one.langitude),float(one.londitude), float(latitude), float(longitude))
                    print(f'{displacement} this is displacement ')
                    if(displacement<=20):
                        ind = True
                        break
            if(ind):
                cseObj = cseData()
                cseObj.roll_no = roll_no
                cseObj.branch = branch
                cseObj.section = section
                cseObj.student_name = name
                cseObj.year = year
                cseObj.subCode = code
                # filter this 
                cseObj.save()
                return Response({'msg':'Data enter Success'}, status=status.HTTP_200_OK)
                # print("Attendance save successfully")
            else:
                # print('something wrong')
                return Response({'errors':{'non_field_errors':['Data is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        elif(branch=="IT"):
            pass
        elif(branch=="ECE"):
            pass
        elif(branch=="MC"):
            pass
    # return render(request, './AttendanceApp/profile.html')


class superUser_view(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer= SuperUserDataSerializerfirst(data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            sub_otp = serializer.data.get('otp')
            s = subOtp()
            londitude1 = serializer.data.get('latitude')
            langitude2 = serializer.data.get('longitude')
            email = serializer.data.get('email')
            s.otp = sub_otp
            s.londitude = londitude1
            s.langitude = langitude2
            s.save()
            send_otp(email, sub_otp)
            return Response({'msg':'Data enter Success and email send successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Data is not Valid Data enter Success and email send successfully']}}, status=status.HTTP_404_NOT_FOUND)


class superUser_next(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer= SuperUserDataSerializersecond(data=request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            branch = serializer.data.get('branch')
            subCode = serializer.data.get('subCode')
            sec = serializer.data.get('section')
            year = serializer.data.get('year')
            sub_otp = serializer.data.get('otp')
            email = serializer.data.get('email')
            # removeotp from object
            code = str(sub_otp)
            
            obj = subOtp.objects.filter(otp=code)
            print(f'{code} jnhbhbb {obj}')
            # obj.delete()
        # print("objext delete successfully")
        # today code for this subject
        # wait 5 min then process all data and delete one by one
        # print('5 min time is over')
            if(branch=="CSE"):
                # print("cse")
                objAll = cseData.objects.all()
                data = []
                count = 1
                for obj in objAll:
                    print(f'{obj.year} and {year} {obj.section} {sec} {subCode} {obj.subCode} {obj.student_name} {obj.roll_no}')
                    if((obj.year==int(year)) and (obj.section == sec) and (obj.subCode==subCode)):
                        print(f'{obj.subCode} and {obj.section} {obj.section}{obj.student_name} {obj.student_name}')
                        data.append({
                            "id":count,
                            "student_name":obj.student_name,
                            "roll_no":obj.roll_no,
                            "year":obj.year,
                            "branch":obj.branch,
                            "section":obj.section,
                            "subCode":obj.subCode,
                            "isPresent":obj.isPresent
                        })
                        # obj.delete()
                        count = count+1
                print(data)
                # send_file(email, data)
                file_path = f"output_{branch}_{sec}_{year}.xlsx"
                pd.DataFrame(data).to_excel(file_path, index=False)

                # #######################################
                receiver_email = email
                # sender_email = "eurekadigital6@gmail.com"
                # password = "yags nldl objv doyv"
                subject = "Email with attachment"
                content = "This is the content of the email."
                send_email_with_attachment(receiver_email, subject, content, file_path)
                # print("Email sent successfully!")
                return Response({'msg':'Data enter Success','getdata': data},status=status.HTTP_200_OK)
        
            elif(branch=="IT"):
                pass
            elif(branch=="ECE"):
                pass
            elif(branch=="MC"):
                pass

            else:
                return Response({'errors':{'non_field_errors':['Data is not Valid']}}, status=status.HTTP_404_NOT_FOUND)

class profileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format= None):
        serializer = SerializeUserData(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class sendEmailotp(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format= None):
        serializer = SerializesendEmail(data=request.data)
        if serializer.is_valid(raise_exception=True):
            otp = serializer.data.get('otp')
            email = serializer.data.get('email')
            send_otp(email, otp)
            return Response({'msg':' email send successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Data is not  email send successfully']}}, status=status.HTTP_404_NOT_FOUND)

class isEmailUpdate(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request, format=None):
    serializer = UpdateIsemail(data=request.data, context={'user':request.user})
    print(serializer)
    serializer.is_valid(raise_exception=True)
    # if serializer.is_valid():
    #     serializer.save()
    return Response({'msg':'Update Successfully'}, status=status.HTTP_200_OK)


class sendData(APIView):
  renderer_classes = [UserRenderer]
  permission_classes = [IsAuthenticated]
  def post(self, request):
        serializer = StudentListSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            data = serializer.data.get('students')
            email = serializer.data.get('email')
            branch = serializer.data.get('branch')
            sec = serializer.data.get('section')
            year = serializer.data.get('year')
            file_path = f"output_{branch}_{sec}_{year}.xlsx"
            print(data)
            pd.DataFrame(data).to_excel(file_path, index=False)
            receiver_email = email
            # sender_email = "eurekadigital6@gmail.com"
            # password = "yags nldl objv doyv"
            subject = "Email with attachment"
            content = "This is the content of the email."
            send_email_with_attachment(receiver_email, subject, content, file_path)
            return Response({'msg':'Email send Successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
