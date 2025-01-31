from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from account.utils import Util
# from models import 

# class signup_viewSerializer(serializers.ModelSerializer):
#   # We are writing this becoz we need confirm password field in our Registratin Request
#   password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
#   class Meta:
#     model = User
#     fields = ['roll_no', 'email','student_name','dob','branch','year','number','password1','password2']
#     extra_kwargs={
#       'password1':{'write_only':True}
#     }

#   # Validating Password and Confirm Password while Registration
#   def validate(self, attrs):
#     password1 = attrs.get('password1')
#     password2 = attrs.get('password2')
#     if password1 != password2:
#       raise serializers.ValidationError("Password and Confirm Password doesn't match")
#     return attrs

#   def create(self, validate_data):
#     return User.objects.create_user(**validate_data)


class signup_viewSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['roll_no', 'email', 'student_name', 'dob', 'branch', 'year', 'number', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password doesn't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    roll_no = serializers.CharField(max_length=10)
    class Meta:
        model = User
        fields = ['roll_no', 'password']

class UserDataSerializer(serializers.Serializer):
    roll_no = serializers.CharField(max_length=10)
    student_name = serializers.CharField(max_length=20)
    branch = serializers.CharField(max_length=50)
    year = serializers.IntegerField()
    section = serializers.CharField(max_length=5)
    subCode = serializers.CharField(max_length=10)
    longitude = serializers.CharField()
    latitude = serializers.CharField()
    otp = serializers.CharField(max_length=10)
    number = serializers.CharField(max_length=10)
    class Meta:
        fields = ['roll_no', 'student_name','branch','year','section','subCode','otp','number','longitude','latitude']


class SuperUserDataSerializerfirst(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    email = serializers.EmailField(max_length=255)
    latitude = serializers.CharField(max_length=30)
    longitude = serializers.CharField(max_length=30)
    class Meta:
        fields = ['email','latitude','longitude','otp']

class SuperUserDataSerializersecond(serializers.Serializer):
    roll_no = serializers.CharField(max_length=10)
    student_name = serializers.CharField(max_length=20)
    branch = serializers.CharField(max_length=50)
    year = serializers.IntegerField()
    section = serializers.CharField(max_length=5)
    subCode = serializers.CharField(max_length=10)
    email = serializers.EmailField(max_length=255)
    otp = serializers.CharField(max_length=6)
    class Meta:
        fields = ['roll_no', 'student_name','branch','year','section','subCode','email','otp']

class SerializesendEmail(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    otp = serializers.CharField(max_length=6)
    class Meta:
        fields = ['email','otp']

class SerializesdataSend(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    data = serializers.CharField(max_length=6)
    class Meta:
        fields = ['email','otp']


class SerializeUserData(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['roll_no', 'student_name','branch','year','email','number','is_staff','is_active','is_superuser','is_email']

class StudentSerializer(serializers.Serializer):
    student_name = serializers.CharField(max_length=255)
    roll_no = serializers.CharField(max_length=20)
    year = serializers.IntegerField()
    branch = serializers.CharField(max_length=100)
    section = serializers.CharField(max_length=10)
    subCode = serializers.CharField(max_length=20)
    isPresent = serializers.BooleanField()

class StudentListSerializer(serializers.Serializer):
    students = StudentSerializer(many=True)
    email = serializers.EmailField(max_length=255)
    section = serializers.CharField(max_length=10)
    year = serializers.IntegerField()
    branch = serializers.CharField(max_length=100)
    
class UpdateIsemail(serializers.ModelSerializer):
    is_email = serializers.BooleanField(default=True)
    class Meta:
        model = User
        fields = ['is_email','dob','year','branch','number']
    def validate(self, attrs):
        is_email = attrs.get('is_email')
        dob = attrs.get('dob')
        year = attrs.get('year')
        branch = attrs.get('branch')
        phone = attrs.get('number')
        user = self.context.get('user')
        
        # raise serializers.ValidationError("Password and Confirm Password doesn't match")
        user.is_email=True
        user.dob=dob
        user.year=year
        user.branch=branch
        user.number=phone
        user.save()
        return attrs