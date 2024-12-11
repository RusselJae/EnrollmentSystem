from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User





class AppCsStudents(models.Model):
    # Directly define fields without inheritance to match existing database structure
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    
    birthdate = models.DateField()
    age = models.IntegerField()
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    mobile_number_validator = RegexValidator(
        regex=r'^\d{11}$', 
        message="Mobile number must be 11 digits"
    )
    mobile_number = models.CharField(
        max_length=11, 
        validators=[mobile_number_validator],
        unique=True
    )
    
    email = models.EmailField(unique=True)
    student_number = models.CharField(max_length=20, unique=True)
    
    PROGRAM_CHOICES = [
        ('BS Computer Science', 'BS Computer Science'),
        ('BS Information Technology', 'BS Information Technology'),
    ]
    
    program = models.CharField(
        max_length=100, 
        choices=PROGRAM_CHOICES,
        verbose_name="Program of Study"
    )
    
    STATUS_CHOICES = [
        ('regular', 'Regular'),
        ('irregular', 'Irregular'),
        ('transferee', 'Transferee'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]
    year_level = models.CharField(max_length=50, choices=YEAR_CHOICES)
    
    section = models.CharField(max_length=50)
    
    FEE_CHOICES = [
        ('paid', 'Paid'),
        ('not paid', 'Not Paid'),
    ]
    soc_fee = models.CharField(max_length=50, choices=FEE_CHOICES)
    
    address = models.CharField(max_length=100)
    
    date_enrolled = models.DateField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        """
        Validate program selection
        """
        # Ensure program is selected from the predefined choices
        if self.program not in dict(self.PROGRAM_CHOICES):
            raise ValidationError({
                'program': 'Invalid program selected. Please choose from the available options.'
            })
    
    def save(self, *args, **kwargs):
        """
        Ensure full validation before saving
        """
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        managed = True  # If this is an existing table
        db_table = 'app_cs_students'
        verbose_name = 'CS Student'
        verbose_name_plural = 'CS Students'
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} (CS - {self.student_number})"

class AppItStudents(models.Model):
    # Directly define fields without inheritance to match existing database structure
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    
    birthdate = models.DateField()
    age = models.IntegerField()
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    mobile_number_validator = RegexValidator(
        regex=r'^\d{11}$', 
        message="Mobile number must be 11 digits"
    )
    mobile_number = models.CharField(
        max_length=11, 
        validators=[mobile_number_validator],
        unique=True
    )
    
    email = models.EmailField(unique=True)
    student_number = models.CharField(max_length=20, unique=True)
    
    PROGRAM_CHOICES = [
        ('BS Computer Science', 'BS Computer Science'),
        ('BS Information Technology', 'BS Information Technology'),
    ]
    
    program = models.CharField(
        max_length=100, 
        choices=PROGRAM_CHOICES,
        verbose_name="Program of Study"
    )
    
    STATUS_CHOICES = [
        ('regular', 'Regular'),
        ('irregular', 'Irregular'),
        ('transferee', 'Transferee'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    ]
    year_level = models.CharField(max_length=2, choices=YEAR_CHOICES)
    
    section = models.CharField(max_length=50)
    
   
    FEE_CHOICES = [
        ('paid', 'Paid'),
        ('not paid', 'Not Paid'),
    ]
    soc_fee = models.CharField(max_length=50, choices=FEE_CHOICES)
    
    date_enrolled = models.DateField(blank=True, null=True)
    
    address = models.CharField(max_length=100)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Validate program selection
        """
        # Ensure program is selected from the predefined choices
        if self.program not in dict(self.PROGRAM_CHOICES):
            raise ValidationError({
                'program': 'Invalid program selected. Please choose from the available options.'
            })
    
    def save(self, *args, **kwargs):
        """
        Ensure full validation before saving
        """
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        managed = True  # If this is an existing table
        db_table = 'app_it_students'
        verbose_name = 'IT Student'
        verbose_name_plural = 'IT Students'
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} (IT - {self.student_number})"
    
    
class AppCsStudentsSub(models.Model):
    student_number = models.IntegerField(unique=True)
    sub1 = models.CharField(max_length=100)
    sub2 = models.CharField(max_length=100)
    sub3 = models.CharField(max_length=100)
    sub4 = models.CharField(max_length=100)
    sub5 = models.CharField(max_length=100)
    sub6 = models.CharField(max_length=100)
    sub7 = models.CharField(max_length=100)
    sub8 = models.CharField(max_length=100)
    sub9 = models.CharField(max_length=100)
    total_units = models.IntegerField()
    semester = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'app_cs_students_sub'
        
class AppItStudentsSub(models.Model):
    student_number = models.IntegerField(unique=True)
    sub1 = models.CharField(max_length=100)
    sub2 = models.CharField(max_length=100)
    sub3 = models.CharField(max_length=100)
    sub4 = models.CharField(max_length=100)
    sub5 = models.CharField(max_length=100)
    sub6 = models.CharField(max_length=100)
    sub7 = models.CharField(max_length=100)
    sub8 = models.CharField(max_length=100)
    sub9 = models.CharField(max_length=100)
    total_units = models.IntegerField()
    semester = models.IntegerField()
    
    class Meta:
        managed = True
        db_table = 'app_it_students_sub'


class AppSub(models.Model):
    sub_code = models.CharField(max_length=50)
    sub_name = models.CharField(max_length=100)
    lab_units = models.IntegerField()
    lec_units = models.IntegerField()
    year_level = models.IntegerField()
    semester = models.IntegerField()
    cs = models.CharField(max_length=50)
    it = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'app_sub'



