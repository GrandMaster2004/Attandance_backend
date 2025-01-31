# Generated by Django 5.0.6 on 2024-11-28 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='cseData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_no', models.CharField(max_length=10)),
                ('student_name', models.CharField(max_length=20)),
                ('branch', models.CharField(max_length=50)),
                ('year', models.IntegerField(max_length=1)),
                ('section', models.CharField(max_length=5)),
                ('otp', models.IntegerField(max_length=6)),
                ('location', models.CharField(max_length=16)),
                ('subCode', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='eceData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_no', models.CharField(max_length=10)),
                ('student_name', models.CharField(max_length=20)),
                ('branch', models.CharField(max_length=50)),
                ('year', models.IntegerField(max_length=1)),
                ('ection', models.CharField(max_length=5)),
                ('otp', models.IntegerField(max_length=6)),
                ('location', models.CharField(max_length=16)),
                ('subCode', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='itData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_no', models.CharField(max_length=10)),
                ('student_name', models.CharField(max_length=20)),
                ('branch', models.CharField(max_length=50)),
                ('year', models.IntegerField(max_length=1)),
                ('ection', models.CharField(max_length=5)),
                ('otp', models.IntegerField(max_length=6)),
                ('location', models.CharField(max_length=16)),
                ('subCode', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='subOtp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='StudentsCustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('roll_no', models.CharField(max_length=10, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('student_name', models.CharField(max_length=50)),
                ('dob', models.DateField()),
                ('branch', models.CharField(max_length=50)),
                ('year', models.IntegerField()),
                ('number', models.CharField(max_length=10, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('otp', models.CharField(max_length=4)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
