import json
from django.http import HttpResponseRedirect
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from datetime import date
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .forms import UserRegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from unittest.mock import patch
from .models import AppCsStudents, AppItStudents,AppCsStudentsSub,AppItStudentsSub,AppSub
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from django.db.models import Q
from itertools import chain




class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        if self.request.user.is_superuser:
            print("Redirecting to admin dashboard")
            return reverse_lazy('admin_dashboard')
        else:
            print("Redirecting to home")
            return reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            print(f"User is authenticated: {self.request.user}")
            return HttpResponseRedirect(self.get_success_url())
        return super().get(request, *args, **kwargs)



class CustomLoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.admin_dashboard_url = reverse('admin_dashboard')
        self.home_url = reverse('home')
        
        # Create a regular user
        self.regular_user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create a superuser
        self.superuser = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )

    def test_login_page_loads(self):
        """Test that login page loads correctly"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_superuser_login_redirect(self):
        """Test that superuser is redirected to admin dashboard after login"""
        response = self.client.post(self.login_url, {
            'username': 'admin',
            'password': 'adminpass123'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.admin_dashboard_url)

    def test_regular_user_login_redirect(self):
        """Test that regular user is redirected to home page after login"""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.home_url)

    def test_invalid_login(self):
        """Test that invalid credentials don't allow login"""
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        
        self.assertEqual(response.status_code, 200)  # Stays on login page
        self.assertTrue(response.context['form'].errors)  # Should have form errors
        
    def tearDown(self):
        # Clean up created users
        User.objects.all().delete()


class RegisterViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }

    def test_register_page_GET(self):
        """Test GET request to registration page"""
        response = self.client.get(self.register_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        self.assertIsInstance(response.context['form'], UserRegisterForm)

    def test_register_successful_POST(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.valid_user_data)
        
        # Check if user was created
        self.assertTrue(User.objects.filter(username='testuser').exists())
        
        # Check if redirected to login page
        self.assertRedirects(response, self.login_url)
        
        # Check if success message was created
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Hi testuser, your account was created successfully')

    def test_register_invalid_POST(self):
        """Test registration with invalid data"""
        # Invalid data missing required fields
        invalid_data = {
            'username': 'testuser',
            'email': 'invalid-email',  # Invalid email format
            'password1': 'test123',
            'password2': 'different123'  # Passwords don't match
        }
        
        response = self.client.post(self.register_url, invalid_data)
        
        # Check that the response goes back to the register page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        
        # Check that no user was created
        self.assertFalse(User.objects.filter(username='testuser').exists())
        
        # Check that form errors are present
        self.assertTrue(response.context['form'].errors)

    def test_register_duplicate_username_POST(self):
        """Test registration with existing username"""
        # Create a user first
        User.objects.create_user(username='testuser', email='existing@example.com', password='testpass123')
        
        # Try to create another user with the same username
        response = self.client.post(self.register_url, self.valid_user_data)
        
        # Check that the response goes back to the register page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
        
        # Check that form has username error
        self.assertIn('username', response.context['form'].errors)
        
        # Check that only one user exists with this username
        self.assertEqual(User.objects.filter(username='testuser').count(), 1)
        
        
class HomeViewTest(TestCase):
    def setUp(self):
        """Set up test client and user"""
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_home_view_get(self):
        """Test that home view returns successful response and uses correct template"""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        


class StudentProfileViewTests(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='oldpassword123',
            first_name='John',
            last_name='Doe'
        )
        
        # URL for the profile view
        self.url = reverse('student_profile')
        
        # Log in the test user
        self.client.login(username='testuser', password='oldpassword123')

    def test_get_profile_page(self):
        """Test GET request to profile page"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_profile.html')

    def test_update_names_only(self):
        """Test updating only first and last names"""
        response = self.client.post(self.url, {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'current_password': 'oldpassword123'
        })
        
        # Check redirect and success message
        self.assertRedirects(response, self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Profile updated successfully.')
        
        # Verify database update
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Jane')
        self.assertEqual(self.user.last_name, 'Smith')

    def test_incorrect_current_password(self):
        """Test with wrong current password"""
        response = self.client.post(self.url, {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'current_password': 'wrongpassword'
        })
        
        # Check redirect and error message
        self.assertRedirects(response, self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Current password is incorrect.')
        
        # Verify no changes were made
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')

    def test_password_change_success(self):
        """Test successful password change"""
        response = self.client.post(self.url, {
            'current_password': 'oldpassword123',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        })
        
        # Check redirect and success message
        self.assertRedirects(response, self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Profile updated successfully.')
        
        # Verify password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword123'))

    def test_password_mismatch(self):
        """Test password change with mismatched new passwords"""
        response = self.client.post(self.url, {
            'current_password': 'oldpassword123',
            'new_password': 'newpassword123',
            'confirm_password': 'differentpassword123'
        })
        
        # Check redirect and error message
        self.assertRedirects(response, self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'New passwords do not match.')
        
        # Verify password was not changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('oldpassword123'))

    def test_password_too_short(self):
        """Test password change with too short new password"""
        response = self.client.post(self.url, {
            'current_password': 'oldpassword123',
            'new_password': 'short',
            'confirm_password': 'short'
        })
        
        # Check redirect and error message
        self.assertRedirects(response, self.url)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Password must be at least 8 characters long.')
        
        # Verify password was not changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('oldpassword123'))

    def test_unauthenticated_access(self):
        """Test access to view when not logged in"""
        # Log out the user
        self.client.logout()
        
        # Try to access the profile page
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 302)
        



class CorViewTest(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client = Client()
        
        # Create test data for CS student with correct choice values
        self.cs_student = AppCsStudents.objects.create(
            student_number=int('CS12345'[2:]),
            email='test@example.com',
            first_name='Test',
            last_name='Student',
            birthdate=date(2000, 1, 1),
            age=23,
            gender='male',  # From GENDER_CHOICES
            mobile_number='09123456789',  # 11 digits as required
            program='BS Computer Science',  # From PROGRAM_CHOICES
            status='regular',  # From STATUS_CHOICES
            year_level='1',  # From YEAR_CHOICES
            section='A',
            soc_fee='paid',  # From FEE_CHOICES
            address='123 Test Street'
        )
        
        # Create test data for IT student with correct choice values
        self.it_student = AppItStudents.objects.create(
            student_number=int('IT12345'[2:]),
            email='test_it@example.com',
            first_name='Test',
            last_name='IT Student',
            birthdate=date(2000, 1, 1),
            age=23,
            gender='female',  # From GENDER_CHOICES
            mobile_number='09987654321',  # 11 digits as required
            program='BS Information Technology',  # From PROGRAM_CHOICES
            status='regular',  # From STATUS_CHOICES
            year_level='1',  # From YEAR_CHOICES
            section='B',
            soc_fee='paid',  # From FEE_CHOICES
            address='456 Test Avenue'
        )
        
        # Create test subjects
        self.test_sub = AppSub.objects.create(
            sub_code='CS101',
            sub_name='Introduction to Programming',
            lec_units=3,
            lab_units=1,
            year_level=1,
            semester=1,
            cs='yes',
            it='no'
        )
        
        self.test_it_sub = AppSub.objects.create(
            sub_code='IT101',
            sub_name='IT Fundamentals',
            lec_units=2,
            lab_units=1,
            year_level=1,
            semester=1,
            cs='no',
            it='yes'
        )
        
        # Create student subjects
        self.cs_student_sub = AppCsStudentsSub.objects.create(
            student_number=int('CS12345'[2:]),  # Convert to integer, removing 'CS' prefix
            sub1='CS101',
            sub2='',
            sub3='',
            sub4='',
            sub5='',
            sub6='',
            sub7='',
            sub8='',
            sub9='',
            total_units=4,
            semester=1,
            encoder='test_encoder'
        )
        
        self.it_student_sub = AppItStudentsSub.objects.create(
            student_number=int('IT12345'[2:]),  # Convert to integer, removing 'IT' prefix
            sub1='IT101',
            sub2='',
            sub3='',
            sub4='',
            sub5='',
            sub6='',
            sub7='',
            sub8='',
            sub9='',
            total_units=3,
            semester=1,
            encoder='test_encoder'
        )

    def test_cs_student_successful_cor(self):
        """Test successful COR retrieval for CS student"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('cor'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cor.html')
        self.assertIn('student', response.context)
        self.assertIn('subjects', response.context)
        self.assertEqual(response.context['total_lec_units'], 3)
        self.assertEqual(response.context['total_lab_units'], 1)
        self.assertEqual(response.context['total_units'], 4)

 
    def test_no_student_record(self):
        """Test when no student record exists"""
        # Change user email to non-existent student
        self.user.email = 'nonexistent@example.com'
        self.user.save()
        
        self.client.force_login(self.user)
        response = self.client.get(reverse('cor'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cor.html')
        # self.assertContains(response, "There's no student found with this email.")

    def test_login_required(self):
        """Test that view requires login"""
        response = self.client.get(reverse('cor'))
        login_url =  reverse('login')
        
        expected_redirect = f'{login_url}?next={reverse('cor')}'
        self.assertRedirects(response, expected_redirect)
        
    def test_it_student_successful_cor(self):
        """Test successful COR retrieval for IT student"""
        # Change user email to IT student email
        self.user.email = 'test_it@example.com'
        self.user.save()
        
        self.client.force_login(self.user)
        response = self.client.get(reverse('cor'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cor.html')
        self.assertIn('student', response.context)
        self.assertIn('subjects', response.context)
        self.assertEqual(response.context['total_lec_units'], 2)
        self.assertEqual(response.context['total_lab_units'], 1)
        self.assertEqual(response.context['total_units'], 3)

    def test_cs_student_not_enrolled(self):
        """Test CS student without subjects"""
        # Delete student subjects
        self.cs_student_sub.delete()
        
        self.client.force_login(self.user)
        response = self.client.get(reverse('cor'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cor.html')
        self.assertContains(response, 'This student is not enrolled yet.')

    def test_it_student_not_enrolled(self):
        """Test IT student without subjects"""
        # Change user email to IT student email
        self.user.email = 'test_it@example.com'
        self.user.save()
        
        # Delete student subjects
        self.it_student_sub.delete()
        
        self.client.force_login(self.user)
        response = self.client.get(reverse('cor'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cor.html')
        self.assertContains(response, 'This student is not enrolled yet.')

    def test_subject_details_calculation(self):
        """Test detailed subject information and calculations"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('cor'))
        
        subjects = response.context['subjects']
        self.assertEqual(len(subjects), 1)  # Only one subject in test data
        
        subject = subjects[0]
        self.assertEqual(subject['subject_code'], 'CS101')
        self.assertEqual(subject['subject_name'], 'Introduction to Programming')
        self.assertEqual(subject['lecture_units'], 3)
        self.assertEqual(subject['lab_units'], 1)
        self.assertEqual(subject['time'], 'TBA')
        self.assertEqual(subject['day'], 'TBA')
        self.assertEqual(subject['room'], 'TBA')
        self.assertEqual(subject['sched'], 'TBA')


class AdminDashboardViewTest(TestCase):
    def setUp(self):
        # Create superuser
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        
        # Create regular user
        self.regular_user = User.objects.create_user(
            username='user',
            password='userpass123'
        )
        
        self.client = Client()
        
        # Create sample CS students
        AppCsStudents.objects.create(
            first_name="John",
            last_name="Doe",
            birthdate=date(2000, 1, 1),
            age=23,
            gender="male",
            mobile_number="09123456789",
            email="john.doe@example.com",
            student_number="2020-CS-001",
            program="BS Computer Science",
            status="regular",
            year_level="1",
            section="A",
            soc_fee="paid",
            address="123 Main St",
            date_enrolled=timezone.now().date()
        )
        
        AppCsStudents.objects.create(
            first_name="Jane",
            last_name="Smith",
            birthdate=date(2001, 2, 2),
            age=22,
            gender="female",
            mobile_number="09123456788",
            email="jane.smith@example.com",
            student_number="2020-CS-002",
            program="BS Computer Science",
            status="irregular",
            year_level="2",
            section="B",
            soc_fee="not paid",
            address="456 Oak St",
            date_enrolled=None
        )
        
        # Create sample IT students
        AppItStudents.objects.create(
            first_name="Bob",
            last_name="Brown",
            birthdate=date(2000, 3, 3),
            age=23,
            gender="male",
            mobile_number="09123456787",
            email="bob.brown@example.com",
            student_number="2020-IT-001",
            program="BS Information Technology",
            status="regular",
            year_level="3",
            section="A",
            soc_fee="paid",
            address="789 Pine St",
            date_enrolled=timezone.now().date()
        )
        
        AppItStudents.objects.create(
            first_name="Alice",
            last_name="Wilson",
            birthdate=date(2001, 4, 4),
            age=22,
            gender="female",
            mobile_number="09123456786",
            email="alice.wilson@example.com",
            student_number="2020-IT-002",
            program="BS Information Technology",
            status="transferee",
            year_level="2",
            section="B",
            soc_fee="not paid",
            address="321 Elm St",
            date_enrolled=None
        )

    def test_admin_dashboard_superuser_access(self):
        """Test that superuser can access the dashboard"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_dashboard.html')

    def test_admin_dashboard_regular_user_access(self):
        """Test that regular user cannot access the dashboard"""
        self.client.login(username='user', password='userpass123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_admin_dashboard_unauthenticated_access(self):
        """Test that unauthenticated user cannot access the dashboard"""
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_admin_dashboard_context_data(self):
        """Test that context data is correct"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_dashboard'))
        
        context = response.context
        
        # Test counts
        self.assertEqual(context['cs_student_count'], 2)
        self.assertEqual(context['it_student_count'], 2)
        self.assertEqual(context['total_students'], 4)
        self.assertEqual(context['enrolled_students'], 2)  # One each from CS and IT
        self.assertEqual(context['unenrolled_students'], 2)  # One each from CS and IT
        self.assertEqual(context['regular_students'], 2)  # One each from CS and IT
        self.assertEqual(context['irregular_students'], 2)  # One irregular CS and one transferee IT

    def test_admin_dashboard_with_archived_students(self):
        """Test that archived students are handled correctly"""
        # Archive one student from each program
        cs_student = AppCsStudents.objects.first()
        it_student = AppItStudents.objects.first()
        
        cs_student.archive()
        it_student.archive()
        
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_dashboard'))
        
        context = response.context
        
        # Verify counts (should not include archived students)
        self.assertEqual(context['cs_student_count'], 2)
        self.assertEqual(context['it_student_count'], 2)
        self.assertEqual(context['total_students'], 4)

    def test_admin_dashboard_with_different_status_combinations(self):
        """Test dashboard with various student status combinations"""
        # Create additional students with different statuses
        AppCsStudents.objects.create(
            first_name="Test",
            last_name="Student",
            birthdate=date(2000, 5, 5),
            age=23,
            gender="male",
            mobile_number="09123456785",
            email="test.student@example.com",
            student_number="2020-CS-003",
            program="BS Computer Science",
            status="transferee",
            year_level="4",
            section="C",
            soc_fee="paid",
            address="test address",
            date_enrolled=timezone.now().date()
        )
        
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_dashboard'))
        
        context = response.context
        
        # Verify updated counts
        self.assertEqual(context['irregular_students'], 3)  # 1 irregular + 2 transferee
        self.assertEqual(context['enrolled_students'], 3)  # Added one more enrolled student

    def test_empty_database(self):
        """Test dashboard with empty database"""
        AppCsStudents.objects.all().delete()
        AppItStudents.objects.all().delete()
        
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('admin_dashboard'))
        
        context = response.context
        
        # All counts should be zero
        self.assertEqual(context['cs_student_count'], 0)
        self.assertEqual(context['it_student_count'], 0)
        self.assertEqual(context['total_students'], 0)
        self.assertEqual(context['enrolled_students'], 0)
        self.assertEqual(context['unenrolled_students'], 0)
        self.assertEqual(context['regular_students'], 0)
        self.assertEqual(context['irregular_students'], 0)
        
        

class AddStudentsViewTests(TestCase):
    def setUp(self):
        # Create superuser for testing
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        self.client = Client()
        self.client.login(username='admin', password='adminpass123')
        
        # Base student data for testing
        self.base_student_data = {
            'first_name': 'John',
            'middle_name': '',  # Optional field
            'last_name': 'Doe',
            'suffix': '',  # Optional field
            'birthdate': '2000-01-01',
            'age': 24,
            'gender': 'male',
            'mobile_number': '09123456789',
            'email': 'john.doe@example.com',
            'program': 'BS Computer Science',
            'status': 'regular',
            'year_level': '2',
            'section': '1',
            'soc_fee': 'paid',
            'address': '123 Test Street'
        }


    def test_section_capacity_limit(self):
        """Test that sections cannot exceed 30 regular students"""
        # Create 30 students in the same section
        for i in range(30):
            AppCsStudents.objects.create(
                **{k: v for k, v in self.base_student_data.items() if k not in ['email', 'mobile_number']},
                email=f'student{i}@test.com',
                mobile_number=f'091234567{str(i).zfill(2)}',
                student_number=f'2025{str(i+1).zfill(5)}'
            )

        # Try to add 31st student
        response = self.client.post(reverse('add-students'), {
            **self.base_student_data,
            'email': 'student31@test.com',
            'mobile_number': '09123456731'
        })

        self.assertEqual(AppCsStudents.objects.filter(section='1').count(), 30)

    def test_irregular_student_no_section(self):
        """Test that irregular students cannot be assigned to sections"""
        response = self.client.post(reverse('add-students'), {
            **self.base_student_data,
            'status': 'irregular',
            'section': '1'
        })

        self.assertEqual(AppCsStudents.objects.count(), 0)

    def test_unique_student_number_across_programs(self):
        """Test that student numbers are unique across both CS and IT programs"""
        # Create CS student
        AppCsStudents.objects.create(
            **{k: v for k, v in self.base_student_data.items() if k not in ['email', 'mobile_number']},
            email='cs@test.com',
            mobile_number='09123456789',
            student_number='202500001'
        )

        # Try to create IT student with same number
        response = self.client.post(reverse('add-students'), {
            **self.base_student_data,
            'program': 'BS Information Technology',
            'email': 'it@test.com',
            'mobile_number': '09123456790',
            'student_number': '202500001'
        })

        self.assertContains(response, "Student with this student number already exists")
        self.assertEqual(AppItStudents.objects.count(), 0)

    def test_mobile_number_validation(self):
        """Test mobile number format validation"""
        invalid_data = {
            **self.base_student_data,
            'mobile_number': '123'  # Invalid format
        }
        
        with self.assertRaises(ValidationError):
            student = AppCsStudents(**invalid_data)
            student.full_clean()

    def test_program_validation(self):
        """Test program choice validation"""
        invalid_data = {
            **self.base_student_data,
            'program': 'Invalid Program'
        }
        
        with self.assertRaises(ValidationError):
            student = AppCsStudents(**invalid_data)
            student.full_clean()



    def test_unauthorized_access(self):
        """Test that non-superusers cannot access the add students page"""
        # Create regular user
        regular_user = User.objects.create_user(
            username='regular',
            password='regular123'
        )
        
        # Login as regular user
        self.client.login(username='regular', password='regular123')
        
        response = self.client.get(reverse('add-students'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        

class ManageStudentsViewTests(TestCase):
    def setUp(self):
        # Create superuser for authentication
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        self.client = Client()
        
        # Create sample students
        self.cs_student1 = AppCsStudents.objects.create(
            first_name='John',
            last_name='Doe',
            birthdate=timezone.now().date(),
            age=20,
            gender='male',
            mobile_number='12345678901',
            email='john.doe@test.com',
            student_number='2021-CS-001',
            program='BS Computer Science',
            status='regular',
            year_level='1',
            section='A',
            soc_fee='paid',
            address='Test Address 1'
        )
        
        self.cs_student2 = AppCsStudents.objects.create(
            first_name='Jane',
            last_name='Smith',
            birthdate=timezone.now().date(),
            age=21,
            gender='female',
            mobile_number='12345678902',
            email='jane.smith@test.com',
            student_number='2021-CS-002',
            program='BS Computer Science',
            status='regular',
            year_level='2',
            section='B',
            soc_fee='not paid',
            address='Test Address 2'
        )
        
        self.it_student = AppItStudents.objects.create(
            first_name='Bob',
            last_name='Johnson',
            birthdate=timezone.now().date(),
            age=22,
            gender='male',
            mobile_number='12345678903',
            email='bob.johnson@test.com',
            student_number='2021-IT-001',
            program='BS Information Technology',
            status='regular',
            year_level='3',
            section='C',
            soc_fee='paid',
            address='Test Address 3'
        )

    def test_login_required(self):
        """Test that the view requires login"""
        response = self.client.get(reverse('manage-students'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page
        
    def test_superuser_required(self):
        """Test that the view requires superuser status"""
        regular_user = User.objects.create_user(
            username='regular',
            password='regular123'
        )
        self.client.login(username='regular', password='regular123')
        response = self.client.get(reverse('manage-students'))
        self.assertEqual(response.status_code, 302)  # Redirects due to insufficient permissions

    def test_successful_access(self):
        """Test successful access by superuser"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('manage-students'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-students.html')

    def test_context_data(self):
        """Test that the view provides correct context data"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('manage-students'))
        
        self.assertIn('students', response.context)
        self.assertIn('program_choices', response.context)
        self.assertIn('selected_program', response.context)
        
        # Verify program choices
        expected_programs = {
            ('BS Computer Science', 'BS Computer Science'),
            ('BS Information Technology', 'BS Information Technology')
        }
        self.assertEqual(set(response.context['program_choices']), expected_programs)

    def test_program_filter(self):
        """Test filtering by program"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(
            reverse('manage-students'),
            {'program': 'BS Computer Science'}
        )
        
        students = list(response.context['students'])
        self.assertEqual(len(students), 2)  # Should only show CS students
        for student in students:
            self.assertEqual(student['program'], 'BS Computer Science')

    def test_search_functionality(self):
        """Test search functionality"""
        self.client.login(username='admin', password='adminpass123')
        
        # Test search by first name
        response = self.client.get(
            reverse('manage-students'),
            {'search': 'john'}
        )
        self.assertEqual(len(list(response.context['students'])), 2)
        
        # Test search by student number
        response = self.client.get(
            reverse('manage-students'),
            {'search': '2021-CS'}
        )
        self.assertEqual(len(list(response.context['students'])), 2)

    def test_archived_students_excluded(self):
        """Test that archived students are excluded"""
        # Archive one student
        self.cs_student1.is_archived = True
        self.cs_student1.save()
        
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('manage-students'))
        
        students = list(response.context['students'])
        student_numbers = [s['student_number'] for s in students]
        self.assertNotIn(self.cs_student1.student_number, student_numbers)
        self.assertIn(self.cs_student2.student_number, student_numbers)

    def test_pagination(self):
        """Test pagination functionality"""
        # Get the current highest student number to avoid conflicts
        existing_students = AppCsStudents.objects.all().order_by('-student_number')
        start_number = 1  # Default start number
        
        if existing_students.exists():
            # Extract the number from the last student number (assumes format '2021-CS-XXX')
            last_number = int(existing_students.first().student_number.split('-')[-1])
            start_number = last_number + 1

        # Create more students to trigger pagination
        for i in range(15):  # Creates 15 more students
            AppCsStudents.objects.create(
                first_name=f'Student{i}',
                last_name=f'Test{i}',
                birthdate=timezone.now().date(),
                age=20,
                gender='male',
                mobile_number=f'1234567{i:04d}',
                email=f'student{i}@test.com',
                student_number=f'2021-CS-{(start_number + i):03d}',  # Generate unique student numbers
                program='BS Computer Science',
                status='regular',
                year_level='1',
                section='A',
                soc_fee='paid',
                address=f'Test Address {i}'
            )
        
        self.client.login(username='admin', password='adminpass123')
        
        # Test first page
        response = self.client.get(reverse('manage-students'))
        self.assertEqual(len(list(response.context['students'])), 10)  # 10 per page
        
        # Test second page
        response = self.client.get(reverse('manage-students'), {'page': 2})
        self.assertTrue(len(list(response.context['students'])) > 0)
        
class EnrollmentStatusViewTest(TestCase):
    def setUp(self):
        # Create superuser for authentication
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='admin123'
        )
        self.client = Client()
        self.client.login(username='admin', password='admin123')

        # Create test subjects
        self.subject = AppSub.objects.create(
            sub_code='CS101',
            sub_name='Intro to Programming',
            lab_units=1,
            lec_units=2,
            year_level=1,
            semester=1,
            cs='required',
            it='required'
        )

        # Create test students
        self.cs_student = AppCsStudents.objects.create(
            first_name='John',
            last_name='Doe',
            birthdate='2000-01-01',
            age=23,
            gender='male',
            mobile_number='09123456789',
            email='john@test.com',
            student_number='202000001',
            program='BS Computer Science',
            status='regular',
            year_level='1',
            section='A',
            soc_fee='paid',
            address='Test Address'
        )

        self.it_student = AppItStudents.objects.create(
            first_name='Jane',
            last_name='Doe',
            birthdate='2000-01-01',
            age=23,
            gender='female',
            mobile_number='09987654321',
            email='jane@test.com',
            student_number='202000002',
            program='BS Information Technology',
            status='regular',
            year_level='1',
            section='A',
            soc_fee='paid',
            address='Test Address'
        )

    def test_enroll_students_sub_view(self):
        """Test the view that displays the enrollment form"""
        response = self.client.get(reverse('enroll-students-sub'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'enroll-students-sub.html')
        self.assertIn('subjects', response.context)
        self.assertIn('subject_range', response.context)

    def test_successful_cs_enrollment(self):
        """Test successful enrollment for CS student"""
        
        enrollment_data = {
            'program': 'BS Computer Science',
            'enrollment_data': {
                'student_number': '202000001',
                'sub1': 'CS101',
                'total_units': 3,
                'semester': 1
            }
        }
        
        response = self.client.post(
            reverse('enroll_student'),
            data=json.dumps(enrollment_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertEqual(response_data['message'], 'Enrollment successful')

    def test_successful_it_enrollment(self):
        """Test successful enrollment for IT student"""
        enrollment_data = {
            'program': 'BS Information Technology',
            'enrollment_data': {
                'student_number': '202000002',
                'sub1': 'CS101',
                'total_units': 3,
                'semester': 1
            }
        }
        
        response = self.client.post(
            reverse('enroll_student'),
            data=json.dumps(enrollment_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])

    def test_enrollment_without_soc_fee(self):
        """Test enrollment attempt when SOC fee is not paid"""
        self.cs_student.soc_fee = 'not paid'
        self.cs_student.save()

        enrollment_data = {
            'program': 'BS Computer Science',
            'enrollment_data': {
                'student_number': '202000001',
                'sub1': 'CS101',
                'total_units': 3,
                'semester': 1
            }
        }
        
        response = self.client.post(
            reverse('enroll_student'),
            data=json.dumps(enrollment_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 403)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])
        self.assertIn('SOC fee', response_data['message'])

    def test_enrollment_invalid_student(self):
        """Test enrollment attempt with non-existent student"""
        enrollment_data = {
            'program': 'BS Computer Science',
            'enrollment_data': {
                'student_number': '999999999',
                'sub1': 'CS101',
                'total_units': 3,
                'semester': 1
            }
        }
        
        response = self.client.post(
            reverse('enroll_student'),
            data=json.dumps(enrollment_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])

    def test_enrollment_invalid_program(self):
        """Test enrollment attempt with invalid program"""
        enrollment_data = {
            'program': 'Invalid Program',
            'enrollment_data': {
                'student_number': '202000001',
                'sub1': 'CS101',
                'total_units': 3,
                'semester': 1
            }
        }
        
        response = self.client.post(
            reverse('enroll_student'),
            data=json.dumps(enrollment_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])

    def test_enrollment_missing_student_number(self):
        """Test enrollment attempt without student number"""
        enrollment_data = {
            'program': 'BS Computer Science',
            'enrollment_data': {
                'sub1': 'CS101',
                'total_units': 3,
                'semester': 1
            }
        }
        
        response = self.client.post(
            reverse('enroll_student'),
            data=json.dumps(enrollment_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])

    def test_unauthorized_access(self):
        """Test access without proper authentication"""
        # Create non-superuser
        regular_user = User.objects.create_user(
            username='regular',
            password='regular123'
        )
        self.client.login(username='regular', password='regular123')

        response = self.client.get(reverse('enroll-students-sub'))
        self.assertEqual(response.status_code, 302)

        enrollment_data = {
            'program': 'BS Computer Science',
            'enrollment_data': {
                'student_number': '202000001',
                'sub1': 'CS101',
                'total_units': 3,
                'semester': 1
            }
        }
        
        response = self.client.post(
            reverse('enroll_student'),
            data=json.dumps(enrollment_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 302)
        
        

class StudentSuvjectsTests(TestCase):
    def setUp(self):
        # Create superuser for authentication
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        self.client = Client()
        self.client.login(username='admin', password='adminpass123')

        # Create test students
        self.cs_student = AppCsStudents.objects.create(
            first_name="John",
            last_name="Doe",
            birthdate="2000-01-01",
            age=23,
            gender="male",
            mobile_number="12345678901",
            email="john@test.com",
            student_number="202000001",
            program="BS Computer Science",
            status="regular",
            year_level="1",
            section="A",
            soc_fee="paid",
            address="Test Address",
            date_enrolled=timezone.now().date()
        )

        self.it_student = AppItStudents.objects.create(
            first_name="Jane",
            last_name="Smith",
            birthdate="2000-01-01",
            age=23,
            gender="female",
            mobile_number="12345678902",
            email="jane@test.com",
            student_number="202000002",
            program="BS Information Technology",
            status="regular",
            year_level="1",
            section="A",
            soc_fee="paid",
            address="Test Address",
            date_enrolled=timezone.now().date()
        )

        # Create test subjects
        self.cs_subjects = AppCsStudentsSub.objects.create(
            student_number=202000001,
            sub1="CS101",
            sub2="CS102",
            sub3="",
            sub4="",
            sub5="",
            sub6="",
            sub7="",
            sub8="",
            sub9="",
            encoder="Test Encoder",
            total_units=6,
            semester=1
        )

        self.it_subjects = AppItStudentsSub.objects.create(
            student_number=202000002,
            sub1="IT101",
            sub2="IT102",
            sub3="",
            sub4="",
            sub5="",
            sub6="",
            sub7="",
            sub8="",
            sub9="",
            encoder="Test Encoder",
            total_units=6,
            semester=1
        )

        # Create some test subjects
        AppSub.objects.create(
            sub_code="CS101",
            sub_name="Introduction to Programming",
            lab_units=1,
            lec_units=2,
            year_level=1,
            semester=1,
            cs="Yes",
            it="No"
        )

    def test_manage_students_sub_view_cs(self):
        """Test the manage_students_sub view for CS program"""
        url = reverse('manage-students-sub', kwargs={
            'program': 'BS Computer Science',
            'student_number': '202000001'
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-students-sub.html')
        self.assertEqual(response.context['program_type'], 'CS')
        self.assertEqual(response.context['existing_student'], self.cs_student)

    def test_manage_students_sub_view_it(self):
        """Test the manage_students_sub view for IT program"""
        url = reverse('manage-students-sub', kwargs={
            'program': 'BS Information Technology',
            'student_number': '202000002'
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage-students-sub.html')
        self.assertEqual(response.context['program_type'], 'IT')
        self.assertEqual(response.context['existing_student'], self.it_student)

    def test_manage_students_sub_invalid_program(self):
        """Test manage_students_sub view with invalid program"""
        url = reverse('manage-students-sub', kwargs={
            'program': 'Invalid Program',
            'student_number': '202000001'
        })
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertRedirects(response, reverse('manage-students'))

    def test_get_student_subjects_cs(self):
        """Test get_student_subjects view for CS student"""
        url = reverse('get_student_subjects', kwargs={'student_number': '202000001'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['program'], 'BS Computer Science')
        self.assertEqual(data['sub1'], 'CS101')
        self.assertEqual(data['sub2'], 'CS102')

    def test_get_student_subjects_it(self):
        """Test get_student_subjects view for IT student"""
        url = reverse('get_student_subjects', kwargs={'student_number': '202000002'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['program'], 'BS Information Technology')
        self.assertEqual(data['sub1'], 'IT101')
        self.assertEqual(data['sub2'], 'IT102')

    def test_get_student_subjects_not_found(self):
        """Test get_student_subjects view with non-existent student"""
        url = reverse('get_student_subjects', kwargs={'student_number': '9999999'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_update_student_subject_cs(self):
        """Test update_student_subject view for CS student"""
        url = reverse('update_student_subject')
        data = {
            'student_number': '202000001',
            'subject_index': 2,
            'new_subject': 'CS103',
            'program': 'BS Computer Science',
            'lecture_hours': 2,
            'lab_hours': 1
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_update_student_subject_it(self):
        """Test update_student_subject view for IT student"""
        url = reverse('update_student_subject')
        data = {
            'student_number': '202000002',
            'subject_index': 2,
            'new_subject': 'IT103',
            'program': 'BS Information Technology',
            'lecture_hours': 2,
            'lab_hours': 1
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_update_student_subject_invalid_program(self):
        """Test update_student_subject view with invalid program"""
        url = reverse('update_student_subject')
        data = {
            'student_number': '202000001',
            'subject_index': 2,
            'new_subject': 'CS103',
            'program': 'Invalid Program',
            'lecture_hours': 2,
            'lab_hours': 1
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertFalse(data['success'])

    def test_unauthenticated_access(self):
        """Test access to views without authentication"""
        self.client.logout()
        
        # Test manage_students_sub view
        url = reverse('manage-students-sub', kwargs={
            'program': 'BS Computer Science',
            'student_number': '202000001'
        })
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test get_student_subjects view
        url = reverse('get_student_subjects', kwargs={'student_number': '2020001'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test update_student_subject view
        url = reverse('update_student_subject')
        data = {
            'student_number': '202000001',
            'subject_index': 2,
            'new_subject': 'CS103',
            'program': 'BS Computer Science'
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 302) 
        

class SearchCorViewTests(TestCase):
    def setUp(self):
        # Create admin user
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        
        # Create test CS student
        self.cs_student = AppCsStudents.objects.create(
            first_name='John',
            last_name='Doe',
            birthdate=date(2000, 1, 1),
            age=23,
            gender='male',
            mobile_number='09123456789',
            email='john@test.com',
            student_number='202300001',
            program='BS Computer Science',
            status='regular',
            year_level='2',
            section='A',
            soc_fee='paid',
            address='Test Address'
        )
        
        # Create CS student subjects
        self.cs_student_sub = AppCsStudentsSub.objects.create(
            student_number=202300001,
            sub1='CS101',
            sub2='CS102',
            sub3='',
            sub4='',
            sub5='',
            sub6='',
            sub7='',
            sub8='',
            sub9='',
            encoder='admin',
            total_units=6,
            semester=1
        )
        
        # Create test subjects
        AppSub.objects.create(
            sub_code='CS101',
            sub_name='Programming 1',
            lab_units=1,
            lec_units=2,
            year_level=2,
            semester=1,
            cs='yes',
            it='no'
        )
        AppSub.objects.create(
            sub_code='CS102',
            sub_name='Data Structures',
            lab_units=1,
            lec_units=2,
            year_level=2,
            semester=1,
            cs='yes',
            it='no'
        )
        
        self.client = Client()
        self.client.login(username='admin', password='adminpass123')
        
    def test_search_with_valid_numeric_student_number(self):
        response = self.client.get(f"{reverse('search_cor')}?search=202300001")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_cor.html')
        self.assertContains(response, 'John')
        self.assertContains(response, 'Doe')
        
    def test_search_with_invalid_student_number_format(self):
        response = self.client.get(f"{reverse('search_cor')}?search=ABC12345")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_cor.html')
        # self.assertContains(response, "There's no student found")
        
    def test_search_nonexistent_student(self):
        response = self.client.get(f"{reverse('search_cor')}?search=99999999")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_cor.html')
        # self.assertContains(response, "There's no student found")
        
    def test_search_without_query(self):
        response = self.client.get(reverse('search_cor'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_cor.html')
        self.assertNotContains(response, "There's no student found")
        
    def test_search_student_without_subjects(self):
        # Create a new student without subjects
        new_student = AppCsStudents.objects.create(
            first_name='Jane',
            last_name='Smith',
            birthdate=date(2000, 1, 1),
            age=23,
            gender='female',
            mobile_number='09987654321',
            email='jane@test.com',
            student_number='202300002',
            program='BS Computer Science',
            status='regular',
            year_level='2',
            section='A',
            soc_fee='paid',
            address='Test Address'
        )
        
        response = self.client.get(f"{reverse('search_cor')}?search=202300002")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search_cor.html')
        # self.assertContains(response, "This student is not enrolled yet")
        
    def test_subject_total_units_calculation(self):
        response = self.client.get(f"{reverse('search_cor')}?search=202300001")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_lec_units'], 4)  # 2 + 2
        self.assertEqual(response.context['total_lab_units'], 2)  # 1 + 1
        self.assertEqual(response.context['total_units'], 6)     # 4 + 2
        
    def test_unauthorized_access(self):
        # Logout admin
        self.client.logout()
        response = self.client.get(reverse('search_cor'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
        
    def test_search_by_email(self):
        response = self.client.get(f"{reverse('search_cor')}?search=john@test.com")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')
        self.assertContains(response, 'Doe')
        
    def test_search_by_name(self):
        response = self.client.get(f"{reverse('search_cor')}?search=John")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')
        self.assertContains(response, 'Doe')
        
        
class ArchiveViewTest(TestCase):
    def setUp(self):
        # Create superuser
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        
        # Create regular user
        self.user = User.objects.create_user(
            username='user',
            email='user@test.com',
            password='userpass123'
        )
        
        # Create test students
        self.cs_student = AppCsStudents.objects.create(
            first_name='John',
            last_name='Doe',
            birthdate='2000-01-01',
            age=23,
            gender='male',
            mobile_number='09123456789',
            email='john.doe@test.com',
            student_number='2020000001',
            program='BS Computer Science',
            status='regular',
            year_level='1',
            section='A',
            soc_fee='paid',
            address='Test Address'
        )
        
        self.it_student = AppItStudents.objects.create(
            first_name='Jane',
            last_name='Smith',
            birthdate='2000-02-02',
            age=23,
            gender='female',
            mobile_number='09987654321',
            email='jane.smith@test.com',
            student_number='2020000002',
            program='BS Information Technology',
            status='regular',
            year_level='1',
            section='A',
            soc_fee='paid',
            address='Test Address'
        )
        
        self.client = Client()

    def test_archive_view_access(self):
        """Test access control for archive view"""
        # Test unauthenticated access
        response = self.client.get(reverse('archive'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test non-superuser access
        self.client.login(username='user', password='userpass123')
        response = self.client.get(reverse('archive'))
        self.assertEqual(response.status_code, 302)  # Redirect due to lack of permissions
        
        # Test superuser access
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('archive'))
        self.assertEqual(response.status_code, 200)

    def test_archive_view_filtering(self):
        """Test archive view filtering functionality"""
        self.client.login(username='admin', password='adminpass123')
        
        # Test program filter
        response = self.client.get(reverse('archive'), {'program': 'BS Computer Science'})
        self.assertEqual(len(response.context['students']), 1)
        self.assertEqual(response.context['students'][0]['student_number'], '2020000001')
        
        # Test search functionality
        response = self.client.get(reverse('archive'), {'search': 'John'})
        self.assertEqual(len(response.context['students']), 1)
        self.assertEqual(response.context['students'][0]['first_name'], 'John')
        
        # Test archived filter
        self.cs_student.archive()
        response = self.client.get(reverse('archive'), {'show_archived': True})
        self.assertEqual(len(response.context['students']), 1)
        self.assertTrue(response.context['students'][0]['is_archived'])

    def test_archive_student_functionality(self):
        """Test archiving a student"""
        self.client.login(username='admin', password='adminpass123')
        
        # Test archiving CS student
        response = self.client.post(reverse('archive_student', kwargs={
            'student_id': self.cs_student.id,
            'program': 'BS Computer Science'
        }))
        self.assertEqual(response.status_code, 302)  # Should redirect
        
        # Verify student is archived
        cs_student = AppCsStudents.objects.get(id=self.cs_student.id)
        self.assertTrue(cs_student.is_archived)
        self.assertIsNotNone(cs_student.archived_at)
        
        # Test archiving IT student
        response = self.client.post(reverse('archive_student', kwargs={
            'student_id': self.it_student.id,
            'program': 'BS Information Technology'
        }))
        self.assertEqual(response.status_code, 302)
        
        # Verify IT student is archived
        it_student = AppItStudents.objects.get(id=self.it_student.id)
        self.assertTrue(it_student.is_archived)
        self.assertIsNotNone(it_student.archived_at)

    def test_restore_student_functionality(self):
        """Test restoring an archived student"""
        self.client.login(username='admin', password='adminpass123')
        
        # Archive students first
        self.cs_student.archive()
        self.it_student.archive()
        
        # Test restoring CS student
        response = self.client.post(reverse('restore_student', kwargs={
            'student_id': self.cs_student.id,
            'program': 'BS Computer Science'
        }))
        self.assertEqual(response.status_code, 302)
        
        # Verify student is restored
        cs_student = AppCsStudents.objects.get(id=self.cs_student.id)
        self.assertFalse(cs_student.is_archived)
        self.assertIsNone(cs_student.archived_at)
        
        # Test restoring IT student
        response = self.client.post(reverse('restore_student', kwargs={
            'student_id': self.it_student.id,
            'program': 'BS Information Technology'
        }))
        self.assertEqual(response.status_code, 302)
        
        # Verify IT student is restored
        it_student = AppItStudents.objects.get(id=self.it_student.id)
        self.assertFalse(it_student.is_archived)
        self.assertIsNone(it_student.archived_at)

    def test_invalid_student_operations(self):
        """Test handling of invalid student IDs and programs"""
        self.client.login(username='admin', password='adminpass123')
        
        # Test archiving non-existent student
        response = self.client.post(reverse('archive_student', kwargs={
            'student_id': 99999,
            'program': 'BS Computer Science'
        }))
        self.assertEqual(response.status_code, 302)
        
        # Test restoring non-existent student
        response = self.client.post(reverse('restore_student', kwargs={
            'student_id': 99999,
            'program': 'BS Information Technology'
        }))
        self.assertEqual(response.status_code, 302)
        


class SectionsViewTest(TestCase):
    def setUp(self):
        # Create a superuser for testing
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )
        self.client = Client()
        
        # Create test data for CS students
        AppCsStudents.objects.create(
            first_name="John",
            last_name="Doe",
            birthdate="2000-01-01",
            age=20,
            gender="male",
            mobile_number="12345678901",
            email="john@test.com",
            student_number="202000001",
            program="BS Computer Science",
            status="regular",
            year_level="1",
            section="A",
            soc_fee="paid",
            address="Test Address"
        )
        
        AppCsStudents.objects.create(
            first_name="Jane",
            last_name="Doe",
            birthdate="2000-01-01",
            age=20,
            gender="female",
            mobile_number="12345678902",
            email="jane@test.com",
            student_number="202000002",
            program="BS Computer Science",
            status="irregular",
            year_level="2",
            section="B",
            soc_fee="paid",
            address="Test Address"
        )
        
        # Create test data for IT students
        AppItStudents.objects.create(
            first_name="Bob",
            last_name="Smith",
            birthdate="2000-01-01",
            age=20,
            gender="male",
            mobile_number="12345678903",
            email="bob@test.com",
            student_number="202000003",
            program="BS Information Technology",
            status="regular",
            year_level="1",
            section="A",
            soc_fee="paid",
            address="Test Address"
        )


    def test_superuser_required(self):
        """Test that the view requires superuser status"""
        # Create regular user
        regular_user = User.objects.create_user(
            username='regular',
            password='regular123'
        )
        self.client.login(username='regular', password='regular123')
        
        response = self.client.get(reverse('sections'))
        self.assertEqual(response.status_code, 302)  # Should redirect

    def test_successful_access(self):
        """Test successful access by superuser"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('sections'))
        self.assertEqual(response.status_code, 200)

    def test_context_data(self):
        """Test that all expected context data is present and correct"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('sections'))
        
        # Test total counts
        self.assertEqual(response.context['cs_student_count'], 2)
        self.assertEqual(response.context['it_student_count'], 1)
        
        # Test enrolled students count
        self.assertEqual(response.context['cs_enrolled_students'], 1)
        self.assertEqual(response.context['it_enrolled_students'], 1)
        
        # Test enrollment breakdown
        cs_breakdown = list(response.context['cs_enrollment_breakdown'])
        self.assertEqual(len(cs_breakdown), 2)  # Should have two different year/section combinations
        
        it_breakdown = list(response.context['it_enrollment_breakdown'])
        self.assertEqual(len(it_breakdown), 1)  # Should have one year/section combination
        
        # Test status breakdown
        cs_status = {item['status']: item['student_count'] 
                    for item in response.context['cs_status_breakdown']}
        self.assertEqual(cs_status['regular'], 1)
        self.assertEqual(cs_status['irregular'], 1)
        
        it_status = {item['status']: item['student_count'] 
                    for item in response.context['it_status_breakdown']}
        self.assertEqual(it_status['regular'], 1)

    def test_empty_database(self):
        """Test view behavior with empty database"""
        # Clear all student records
        AppCsStudents.objects.all().delete()
        AppItStudents.objects.all().delete()
        
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('sections'))
        
        self.assertEqual(response.context['cs_student_count'], 0)
        self.assertEqual(response.context['it_student_count'], 0)
        self.assertEqual(response.context['cs_enrolled_students'], 0)
        self.assertEqual(response.context['it_enrolled_students'], 0)