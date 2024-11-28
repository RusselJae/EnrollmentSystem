from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit, Row, Column
from django.utils import timezone
from .models import AppCsStudents, AppItStudents
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomCheckbox(Field):
    template = 'enroll.html'


STATES = (
    ('', 'Choose...'),
    ('MG', 'Minas Gerais'),
    ('SP', 'Sao Paulo'),
    ('RJ', 'Rio de Janeiro')
)

class AddressForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput())
    address_1 = forms.CharField(
        label='Address',
        widget=forms.TextInput(attrs={'placeholder': '1234 Main St'})
    )
    address_2 = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Apartment, studio, or floor'}),
        required=False
    )
    city = forms.CharField()
    state = forms.ChoiceField(choices=STATES)
    zip_code = forms.CharField(label='Zip')
    check_me_out = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'address_1',
            'address_2',
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('zip_code', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            'check_me_out',
            Submit('submit', 'Sign in')
        )

class CustomFieldForm(AddressForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'address_1',
            'address_2',
            Row(
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('state', css_class='form-group col-md-4 mb-0'),
                Column('zip_code', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Field('check_me_out', template='enroll.html'),  # Custom template for the checkbox
            Submit('submit', 'Sign in')
        )
        
        
        


class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        model_class = kwargs.pop('model_class', None)
        super().__init__(*args, **kwargs)
        
        # Dynamically set the model
        if model_class:
            self.Meta.model = model_class
    
    def clean_email(self):
        email = self.cleaned_data['email']
        # Check for unique email across both models
        cs_email_exists = AppCsStudents.objects.filter(email=email).exists()
        it_email_exists = AppItStudents.objects.filter(email=email).exists()
        
        # Exclude the current student's email from the check
        if self.instance:
            cs_email_exists = cs_email_exists and self.instance.email != email
            it_email_exists = it_email_exists and self.instance.email != email
        
        if cs_email_exists or it_email_exists:
            raise ValidationError("This email is already in use.")
        
        return email

    class Meta:
        # This will be dynamically set in __init__
        model = None
        fields = [
            'first_name', 'middle_name', 'last_name', 'suffix',
            'birthdate', 'age', 'gender', 'mobile_number', 
            'email', 'student_number', 'program', 'status', 
            'year_level', 'section', 'profile_image'
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

    # Profile image field
    profile_image = forms.ImageField(
        required=False,
        help_text="Upload a profile image (optional)"
    )

    class Meta:
        model = AppCsStudents  # Assuming this is your model
        fields = [
            'first_name', 'middle_name', 'last_name', 'suffix',
            'birthdate', 'age', 'gender', 'student_number',
            'mobile_number', 'email', 'program', 'status', 
            'year_level', 'section', 'profile_image'
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