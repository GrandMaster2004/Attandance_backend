# Generated by Django 5.0.6 on 2025-01-24 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AttendanceApp', '0010_studentscustomuser_is_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentscustomuser',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
    ]
