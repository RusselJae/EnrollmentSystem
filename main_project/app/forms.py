from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from .models import AppCsStudents, AppItStudents
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        
    
class StudentRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        model_class = kwargs.pop('model_class', None)
        super().__init__(*args, **kwargs)
        
        # Dynamically set the model
        if model_class:
            self.Meta.model = model_class
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        # Check for email existence in both tables
        cs_email_exists = AppCsStudents.objects.filter(email=email).exists()
        it_email_exists = AppItStudents.objects.filter(email=email).exists()
        
        # Exclude the current instance's email during the validation
        if self.instance and self.instance.pk:
            if isinstance(self.instance, AppCsStudents):
                cs_email_exists = AppCsStudents.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
            elif isinstance(self.instance, AppItStudents):
                it_email_exists = AppItStudents.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
        
        # Raise error if email exists in either table
        if cs_email_exists or it_email_exists:
            raise ValidationError("This email is already in use across the system.")
        
        return email

    class Meta:
        # This will be dynamically set in __init__
        model = None
        fields = [
            'first_name', 'middle_name', 'last_name', 'suffix',
            'birthdate', 'age', 'gender', 'mobile_number', 
            'email', 'student_number', 'program', 'status', 
            'year_level', 'section', 'soc_fee', 'address'
        ]
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
            'profile_image': forms.FileInput()
        }
        
        
class StudentUpdateForm(forms.ModelForm):
    """
    Comprehensive form for updating student information including profile image
    """
    # Custom phone number validator
    mobile_number = forms.CharField(
        validators=[RegexValidator(
            regex=r'^[0-9]{11}$', 
            message="Mobile number must be 11 digits"
        )],
        required=True,
        max_length=11
    )

    # Email validation
    email = forms.EmailField(
        validators=[EmailValidator()],
        required=True
    )

    # Custom birthdate validation
    birthdate = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )


    class Meta:
        model = AppCsStudents  # Assuming this is your model
        fields = [
            'first_name', 'middle_name', 'last_name', 'suffix',
            'birthdate', 'age', 'gender', 'student_number',
            'mobile_number', 'email', 'program', 'status', 
            'year_level', 'section', 'soc_fee' , 'date_enrolled', 'address'
        ]

    def clean_birthdate(self):
        """
        Validate birthdate
        """
        birthdate = self.cleaned_data.get('birthdate')
        if birthdate:
            # Calculate age
            today = timezone.now().date()
            age = today.year - birthdate.year - (
                (today.month, today.day) < (birthdate.month, birthdate.day)
            )
            
            # Age validation
            if age < 16 or age > 100:
                raise ValidationError("Invalid birthdate. Age must be between 16 and 100.")
        
        return birthdate

    def clean_age(self):
        """
        Ensure age matches birthdate
        """
        age = self.cleaned_data.get('age')
        birthdate = self.cleaned_data.get('birthdate')
        
        if birthdate:
            today = timezone.now().date()
            calculated_age = today.year - birthdate.year - (
                (today.month, today.day) < (birthdate.month, birthdate.day)
            )
            
            if age != calculated_age:
                raise ValidationError("Age does not match birthdate.")
        
        return age
    
    def clean_email(self):
        email = self.cleaned_data['email']
        
        # Check for email existence in both tables
        cs_email_exists = AppCsStudents.objects.filter(email=email).exists()
        it_email_exists = AppItStudents.objects.filter(email=email).exists()
        
        # Exclude the current instance's email during the validation
        if self.instance and self.instance.pk:
            if isinstance(self.instance, AppCsStudents):
                cs_email_exists = AppCsStudents.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
            elif isinstance(self.instance, AppItStudents):
                it_email_exists = AppItStudents.objects.filter(email=email).exclude(pk=self.instance.pk).exists()
        
        # Raise error if email exists in either table
        if cs_email_exists or it_email_exists:
            raise ValidationError("This email is already in use across the system.")
        
        return email
    
    