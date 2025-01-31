from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, roll_no, email=None, password=None, **extra_fields):
        if not roll_no:
            raise ValueError("The Roll number must be set")
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(roll_no=roll_no, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, roll_no, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        # Ensure that all required fields for a superuser are set
        extra_fields['dob'] = extra_fields.get('dob', '2100-01-01') # Provide a default value or handle appropriately 
        extra_fields['student_name'] = extra_fields.get('student_name', 'admin') 
        extra_fields['branch'] = extra_fields.get('branch', 'admin') 
        extra_fields['year'] = extra_fields.get('year', 1) 
        extra_fields['number'] = extra_fields.get('number', '1334567890') 
        # extra_fields['user_img'] = extra_fields.get('user_img', '')

        return self.create_user(roll_no, email, password, **extra_fields)
