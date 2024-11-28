from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import Http404, HttpResponseRedirect
from .forms import CustomFieldForm
from .models import AppCsStudents, AppItStudents
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import StudentUpdateForm 
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from datetime import date
import json
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os


# Create your views here.
def home(request):
    return render(request, "home.html")

def base4(request):
    return render(request, "base4.html")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')


@login_required()
def profile(request):
    return render(request, 'profile.html')

def dashboard(request):
    return render(request, "dashboard.html")

def dashboard1(request):
    return render(request, "dashboard1.html")

# @login_required()
def ADD_STUDENT(request):
    if request.method == "POST":
        try:
            # Extract form data
            first_name = request.POST['first_name']
            middle_name = request.POST.get('middle_name', '')
            last_name = request.POST['last_name']
            suffix = request.POST.get('suffix', '')
            birthdate = request.POST['birthdate']
            age = request.POST['age']
            gender = request.POST['gender']
            mobile_number = request.POST['mobile_number']
            email = request.POST['email']
            student_number = request.POST['student_number']
            program = request.POST['program']
            status = request.POST['status']
            year_level = request.POST['year_level']
            section = request.POST['section']
            profile_image = request.FILES.get('profile_image')

            # Determine which model to use based on program
            if program == 'BS Computer Science':
                student_obj = AppCsStudents(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    suffix=suffix,
                    birthdate=birthdate,
                    age=age,
                    gender=gender,
                    mobile_number=mobile_number,
                    email=email,
                    student_number=student_number,
                    program=program,
                    status=status,
                    year_level=year_level,
                    section=section,
                    profile_image=profile_image
                )
            elif program == 'BS Information Technology':
                student_obj = AppItStudents(
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    suffix=suffix,
                    birthdate=birthdate,
                    age=age,
                    gender=gender,
                    mobile_number=mobile_number,
                    email=email,
                    student_number=student_number,
                    program=program,
                    status=status,
                    year_level=year_level,
                    section=section,
                    profile_image=profile_image
                )
            else:
                # Handle other programs or raise an error
                messages.error(request, "Invalid program selected")
                return render(request, 'add-students.html')

            # Save the student object
            student_obj.save()
            messages.success(request, "Student details have been created successfully")
            return redirect('add-students')

        except IntegrityError:
            messages.error(request, "Student with this email or student number already exists")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    
    return render(request, 'add-students.html')


def MANAGE_STUDENTS(request):
    # Fetch students from both models
    cs_students = AppCsStudents.objects.all().values(
        'id', 'first_name', 'middle_name', 'last_name', 'suffix', 
        'student_number', 'program', 'year_level', 'section', 
        'email', 'mobile_number', 'status'
    )
    it_students = AppItStudents.objects.all().values(
        'id', 'first_name', 'middle_name', 'last_name', 'suffix', 
        'student_number', 'program', 'year_level', 'section', 
        'email', 'mobile_number', 'status'
    )
    
    # Combine students
    combined_students = list(cs_students) + list(it_students)
    
    # Add a type identifier to distinguish between CS and IT students
    for student in combined_students:
        student['type'] = 'CS' if student in cs_students else 'IT'
    
    # Program filtering
    program_choices = AppCsStudents.PROGRAM_CHOICES  # Both models have same choices
    selected_program = request.GET.get('program', '')
    
    # Filter by program if selected
    if selected_program:
        combined_students = [
            student for student in combined_students 
            if student['program'] == selected_program
        ]
    
    # Sort students
    combined_students.sort(key=lambda x: x['student_number'])
    
    # Pagination
    paginator = Paginator(combined_students, 10)  # 10 students per page
    page_number = request.GET.get('page')
    
    try:
        students = paginator.page(page_number)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    
    context = {
        'students': students,
        'program_choices': program_choices,
        'selected_program': selected_program
    }
    
    return render(request, 'manage-students.html', context)



def update_students(request, student_id):
    """
    View for updating student information with integrated profile image upload
    """
    # Fetch the student object from either AppCsStudents or AppItStudents
    try:
        student = AppCsStudents.objects.get(pk=student_id)
    except AppCsStudents.DoesNotExist:
        try:
            student = AppItStudents.objects.get(pk=student_id)
        except AppItStudents.DoesNotExist:
            raise Http404("Student not found")

    # Initial context for template
    context = {
        'student': student
    }

    if request.method == "POST":
        form = StudentUpdateForm(
            request.POST, 
            request.FILES,  # Important for file uploads 
            instance=student
        )
        
        if form.is_valid():
            try:
                # Handle profile image upload/replacement
                if 'profile_image' in request.FILES:
                    # Delete existing image if it exists
                    if student.profile_image:
                        student.profile_image.delete()
                    
                    # Assign new image
                    student.profile_image = request.FILES['profile_image']
                
                # Save the updated student information
                updated_student = form.save()
                
                messages.success(
                    request, 
                    f"Student {updated_student.student_number} updated successfully"
                )
                return redirect('manage-students')  # Redirect to student management page
            
            except Exception as e:
                messages.error(
                    request, 
                    f"Error updating student: {str(e)}"
                )
        else:
            # Form validation failed
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    
    else:
        # GET request - initial form load
        form = StudentUpdateForm(instance=student)
    
    context['form'] = form
    return render(request, 'update-students.html', context)


def delete_student(request, student_id): 
    
    try:
        student = AppCsStudents.objects.get(id=student_id)
    except AppCsStudents.DoesNotExist:
        try:
            student = AppItStudents.objects.get(id=student_id)
        except AppItStudents.DoesNotExist:
            raise Http404("Student not found in either CS or IT student tables")
    
    if request.method == 'POST': 
        student.delete() 
        messages.success(request, 'Student deleted successfully!') 
        return redirect('manage-students') 
    # return render(request, 'delete_student_confirm.html', {'student': student})


def UPDATE_STUDENTS(request):
    return render(request, "update-students.html")

# def cstable(request):
#     cs_students = CsStudents.objects.all()
#     context = {
#         'cs_students': cs_students
#     }
#     return render(request, "cstable.html", context)

def checklist(request):
    return render(request, "checklist.html")

def enroll(request):
    if request.method == "POST":
        form = CustomFieldForm(request.POST)
        if form.is_valid():
            # Process form data
            # For now, just redirect to a success page or the same page
            return HttpResponseRedirect('enroll')  # Change '/success/' to your desired URL
    else:
        form = CustomFieldForm()
    
    return render(request, "enroll.html", {"form": form})

