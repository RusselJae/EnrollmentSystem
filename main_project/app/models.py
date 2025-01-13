from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.utils import timezone
from django.contrib.auth.models import User

class AppCsStudents(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True, default='')
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10, blank=True, null=True, default='')
    
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
    
    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)
    
    def get_full_name(self):
        """
        Returns the full name of the student, excluding None or blank fields.
        """
        parts = [self.first_name, self.middle_name, self.last_name, self.suffix]
        return " ".join(filter(None, parts))

    def clean(self):
        """
        Validate program selection
        """
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

    def archive(self):
        """
        Method to archive the student
        """
        from django.utils import timezone
        self.is_archived = True
        self.archived_at = timezone.now()
        self.save()

    def restore(self):
        """
        Method to restore an archived student
        """
        self.is_archived = False
        self.archived_at = None
        self.save()

    class Meta:
        managed = True  # If this is an existing table
        db_table = 'app_cs_students'
        verbose_name = 'CS Student'
        verbose_name_plural = 'CS Students' 
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} (CS - {self.student_number})"

class AppItStudents(models.Model):
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True, default='')
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10, blank=True, null=True, default='')
    
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

    is_archived = models.BooleanField(default=False)
    archived_at = models.DateTimeField(null=True, blank=True)
    
    def get_full_name(self):
        """
        Returns the full name of the student, excluding None or blank fields.
        """
        parts = [self.first_name, self.middle_name, self.last_name, self.suffix]
        return " ".join(filter(None, parts))

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

    def archive(self):
        """
        Method to archive the student
        """
        from django.utils import timezone
        self.is_archived = True
        self.archived_at = timezone.now()
        self.save()

    def restore(self):
        """
        Method to restore an archived student
        """
        self.is_archived = False
        self.archived_at = None
        self.save()

    class Meta:
        managed = True  # If this is an existing table
        db_table = 'app_it_students'
        verbose_name = 'IT Student'
        verbose_name_plural = 'IT Students'
        
    def __str__(self):
        return f"{self.first_name} {self.last_name} (IT - {self.student_number})"
    
        
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
    encoder = models.CharField(max_length=100)
    total_units = models.IntegerField()
    semester = models.IntegerField()
    
    class Meta:
        managed = True
        db_table = 'app_it_students_sub'

        
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
    encoder = models.CharField(max_length=100)
    total_units = models.IntegerField()
    semester = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'app_cs_students_sub'

class AppSub(models.Model):
    sub_code = models.CharField(max_length=50)
    sub_name = models.CharField(max_length=100)
    lab_units = models.IntegerField()
    lec_units = models.IntegerField()
    year_level = models.IntegerField()
    semester = models.IntegerField()
    prerequisite = models.CharField(max_length=200)
    cs = models.CharField(max_length=50)
    it = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'app_sub'

class AppCsChecklist(models.Model):
    student_number = models.IntegerField(db_column='student number', unique=True)  # Field renamed to remove unsuitable characters.
    gned_02 = models.DecimalField(db_column='GNED 02', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_05 = models.DecimalField(db_column='GNED 05', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_11 = models.DecimalField(db_column='GNED 11', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_50 = models.DecimalField(db_column='COSC 50', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_21 = models.DecimalField(db_column='DCIT 21', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_22 = models.DecimalField(db_column='DCIT 22', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_1 = models.DecimalField(db_column='FITT 1', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nstp_1 = models.DecimalField(db_column='NSTP 1', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cvsu_101 = models.DecimalField(db_column='CvSU 101', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_01 = models.DecimalField(db_column='GNED 01', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_03 = models.DecimalField(db_column='GNED 03', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_06 = models.DecimalField(db_column='GNED 06', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_12 = models.DecimalField(db_column='GNED 12', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_23 = models.DecimalField(db_column='DCIT 23', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_50 = models.DecimalField(db_column='ITEC 50', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_2 = models.DecimalField(db_column='FITT 2', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nstp_2 = models.DecimalField(db_column='NSTP 2', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_04 = models.DecimalField(db_column='GNED 04', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    math_1 = models.DecimalField(db_column='MATH 1', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_55 = models.DecimalField(db_column='COSC 55', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_60 = models.DecimalField(db_column='COSC 60', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_50 = models.DecimalField(db_column='DCIT 50', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_24 = models.DecimalField(db_column='DCIT 24', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    insy_50 = models.DecimalField(db_column='INSY 50', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_3 = models.DecimalField(db_column='FITT 3', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_08 = models.DecimalField(db_column='GNED 08', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_14 = models.DecimalField(db_column='GNED 14', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    math_2 = models.DecimalField(db_column='MATH 2', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_65 = models.DecimalField(db_column='COSC 65', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_70 = models.DecimalField(db_column='COSC 70', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_25 = models.DecimalField(db_column='DCIT 25', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_55 = models.DecimalField(db_column='DCIT 55', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_4 = models.DecimalField(db_column='FITT 4', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    math_3 = models.DecimalField(db_column='MATH 3', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_75 = models.DecimalField(db_column='COSC 75', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_80 = models.DecimalField(db_column='COSC 80', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_85 = models.DecimalField(db_column='COSC 85', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_101 = models.DecimalField(db_column='COSC 101', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_26 = models.DecimalField(db_column='DCIT 26', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_65 = models.DecimalField(db_column='DCIT 65', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_09 = models.DecimalField(db_column='GNED 09', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    math_4 = models.DecimalField(db_column='MATH 4', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_90 = models.DecimalField(db_column='COSC 90', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_95 = models.DecimalField(db_column='COSC 95', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_106 = models.DecimalField(db_column='COSC 106', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_60 = models.DecimalField(db_column='DCIT 60', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_85 = models.DecimalField(db_column='ITEC 85', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_199 = models.DecimalField(db_column='COSC 199', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_80 = models.DecimalField(db_column='ITEC 80', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_100 = models.DecimalField(db_column='COSC 100', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_105 = models.DecimalField(db_column='COSC 105', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_111 = models.DecimalField(db_column='COSC 111', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_200a = models.DecimalField(db_column='COSC 200A', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_07 = models.DecimalField(db_column='GNED 07', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_10 = models.DecimalField(db_column='GNED 10', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_110 = models.DecimalField(db_column='COSC 110', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_200b = models.DecimalField(db_column='COSC 200B', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'app_cs_checklist'
        
        
class AppItChecklist(models.Model):
    student_number = models.IntegerField(db_column='student number', unique=True)  # Field renamed to remove unsuitable characters.
    gned_02 = models.DecimalField(db_column='GNED 02', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_05 = models.DecimalField(db_column='GNED 05', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_11 = models.DecimalField(db_column='GNED 11', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cosc_50 = models.DecimalField(db_column='COSC 50', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_21 = models.DecimalField(db_column='DCIT 21', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_22 = models.DecimalField(db_column='DCIT 22', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_1 = models.DecimalField(db_column='FITT 1', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nstp_1 = models.DecimalField(db_column='NSTP 1', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    cvsu_101 = models.DecimalField(db_column='CvSU 101', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_01 = models.DecimalField(db_column='GNED 01', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_03 = models.DecimalField(db_column='GNED 03', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_06 = models.DecimalField(db_column='GNED 06', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_12 = models.DecimalField(db_column='GNED 12', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_23 = models.DecimalField(db_column='DCIT 23', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_50 = models.DecimalField(db_column='ITEC 50', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_2 = models.DecimalField(db_column='FITT 2', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nstp_2 = models.DecimalField(db_column='NSTP 2', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_04 = models.DecimalField(db_column='GNED 04', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_07 = models.DecimalField(db_column='GNED 07', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_10 = models.DecimalField(db_column='GNED 10', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_14 = models.DecimalField(db_column='GNED 14', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_55 = models.DecimalField(db_column='ITEC 55', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_24 = models.DecimalField(db_column='DCIT 24', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_50 = models.DecimalField(db_column='DCIT 50', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_3 = models.DecimalField(db_column='FITT 3', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_08 = models.DecimalField(db_column='GNED 08', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_25 = models.DecimalField(db_column='DCIT 25', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_60 = models.DecimalField(db_column='ITEC 60', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_65 = models.DecimalField(db_column='ITEC 65', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_55 = models.DecimalField(db_column='DCIT 55', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_70 = models.DecimalField(db_column='ITEC 70', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    fitt_4 = models.DecimalField(db_column='FITT 4', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    stat_2 = models.DecimalField(db_column='STAT 2', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_75 = models.DecimalField(db_column='ITEC 75', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_80 = models.DecimalField(db_column='ITEC 80', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_85 = models.DecimalField(db_column='ITEC 85', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_90 = models.DecimalField(db_column='ITEC 90', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    insy_55 = models.DecimalField(db_column='INSY 55', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_26 = models.DecimalField(db_column='DCIT 26', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_60 = models.DecimalField(db_column='DCIT 60', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    gned_09 = models.DecimalField(db_column='GNED 09', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_95 = models.DecimalField(db_column='ITEC 95', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_101 = models.DecimalField(db_column='ITEC 101', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_106 = models.DecimalField(db_column='ITEC 106', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_100 = models.DecimalField(db_column='ITEC 100', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_105 = models.DecimalField(db_column='ITEC 105', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_200a = models.DecimalField(db_column='ITEC 200A', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    dcit_65 = models.DecimalField(db_column='DCIT 65', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_111 = models.DecimalField(db_column='ITEC 111', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_116 = models.DecimalField(db_column='ITEC 116', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_110 = models.DecimalField(db_column='ITEC 110', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_200b = models.DecimalField(db_column='ITEC 200B', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    itec_199 = models.DecimalField(db_column='ITEC 199', max_digits=3, decimal_places=2, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'app_it_checklist'

class AppDcsAdmission(models.Model):
    student_number = models.IntegerField(unique=True)

    class Meta:
        managed = False
        db_table = 'app_dcs_admission'