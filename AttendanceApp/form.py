from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()

class StudentForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['roll_no', 'email','student_name','dob','branch','year','number']