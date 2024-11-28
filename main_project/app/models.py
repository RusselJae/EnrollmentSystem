from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.utils import timezone

# Create your models here.
# class AppCsStudents(models.Model):
#     student_number = models.IntegerField()
#     first_name = models.CharField(max_length=50)
#     middle_name = models.CharField(db_column='middle name', max_length=50, blank=True, null=True)  # Field renamed to remove unsuitable characters.
#     last_name = models.CharField(db_column='last name', max_length=50)  # Field renamed to remove unsuitable characters.
#     course = models.CharField(max_length=50)
#     year_level = models.IntegerField()
#     section = models.IntegerField()
#     status = models.CharField(max_length=50)
#     enrollment_status = models.CharField(max_length=50)

#     class Meta:
#         managed = False
#         db_table = 'app_cs_students'


# class AppItStudents(models.Model):
#     student_number = models.IntegerField()
#     first_name = models.CharField(max_length=50)
#     middle_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     course = models.CharField(max_length=50)
#     year_level = models.CharField(max_length=50)
#     section = models.CharField(max_length=50)
#     status = models.CharField(max_length=50)
#     enrollment_status = models.CharField(max_length=50)

#     class Meta:
#         managed = False
#         db_table = 'app_it_students'


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
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
        ('5', '5th Year'),
    ]
    year_level = models.CharField(max_length=50, choices=YEAR_CHOICES)
    
    section = models.CharField(max_length=50)
    
    profile_image = models.ImageField(
        upload_to='student_profiles/', 
        null=True, 
        blank=True
    )
    
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
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    YEAR_CHOICES = [
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
        ('5', '5th Year'),
    ]
    year_level = models.CharField(max_length=2, choices=YEAR_CHOICES)
    
    section = models.CharField(max_length=50)
    
    profile_image = models.ImageField(
        upload_to='student_profiles/', 
        null=True, 
        blank=True
    )
    
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