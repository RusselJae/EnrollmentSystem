from datetime import timezone
from itertools import chain
from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.admin import AdminSite
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.http import Http404, HttpResponseRedirect
from .models import AppCsStudents, AppCsStudentsSub, AppItStudents, AppItStudentsSub, AppSub
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import StudentUpdateForm, UserRegisterForm
from django.contrib import messages
from django.core.files.storage import default_storage
from django.db.models import Value, CharField, Q, Count # Import for annotations
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Max
from django.utils.timezone import now
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView




# Create your views here.
def home(request):
    return render(request, "home.html")

def base4(request):
    return render(request, "base4.html")

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Make sure this matches your template name

    def get_success_url(self):
        # Check if the logged-in user is a superuser
        if self.request.user.is_superuser:
            return reverse_lazy('dashboard1')  # Replace with your dashboard URL name
        else:
            return reverse_lazy('home')  # Replace with your home page URL name

def doLogout(request):
    logout(request)
    request.session.flush()  # Clear the session including CSRF token
    return redirect('login')

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
    # Count CS students
    cs_student_count = AppCsStudents.objects.count()
    
    # Count IT students
    it_student_count = AppItStudents.objects.count()
    
    enrolled_students = (
        AppCsStudents.objects.exclude(date_enrolled__isnull=True).count() + 
        AppItStudents.objects.exclude(date_enrolled__isnull=True).count()
    )
    
    # Unenrolled students (from both tables)
    unenrolled_students = (
        AppCsStudents.objects.filter(date_enrolled__isnull=True).count() + 
        AppItStudents.objects.filter(date_enrolled__isnull=True).count()
    )
    
    # Combine irregular and transferee students as irregular
    regular_students = (
        AppCsStudents.objects.filter(status='regular').count() + 
        AppItStudents.objects.filter(status='regular').count()
    )
    
    irregular_students = (
        AppCsStudents.objects.filter(status__in=['irregular', 'transferee']).count() + 
        AppItStudents.objects.filter(status__in=['irregular', 'transferee']).count()
    )
    
    # Prepare context to pass to the template
    context = {
        'cs_student_count': cs_student_count,
        'it_student_count': it_student_count,
        'total_students': cs_student_count + it_student_count,
        'enrolled_students': enrolled_students,
        'unenrolled_students': unenrolled_students,
        'regular_students': regular_students,
        'irregular_students': irregular_students
    }
    
    return render(request, "dashboard1.html", context)
    
    return render(request, "dashboard1.html", context)

# @login_required()
def generate_student_number():
    """Generates a new student number starting with the current year and a 5-digit auto-incremented number."""
    current_year = now().year
    base_student_number = f"{current_year}00001"

    # Get the max student number from both tables
    max_cs = AppCsStudents.objects.aggregate(max_student_number=Max('student_number'))['max_student_number']
    max_it = AppItStudents.objects.aggregate(max_student_number=Max('student_number'))['max_student_number']

    # Ensure max values are valid integers or set to 0 if None
    max_cs = int(max_cs) if max_cs and str(max_cs).startswith(str(current_year)) else 0
    max_it = int(max_it) if max_it and str(max_it).startswith(str(current_year)) else 0

    # Determine the highest existing student number
    max_existing = max(max_cs, max_it)

    # Generate the next student number
    if max_existing > 0:
        next_student_number = str(max_existing + 1)
    else:
        next_student_number = base_student_number

    return next_student_number


def ADD_STUDENT(request):
    if request.method == "POST":
        form_data = request.POST.dict()  # Collect form data to repopulate on error
        try:
            with transaction.atomic():
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
                program = request.POST['program']
                status = request.POST['status']
                year_level = request.POST['year_level']
                soc_fee = request.POST['soc_fee']
                address = request.POST['address']

                # Generate student number for first-year or transferee students
                if year_level == "1" or status.lower() == "transferee":
                    student_number = generate_student_number()
                    section = None  # No section for first-year or transferee students
                else:
                    student_number = request.POST['student_number']
                    section = request.POST['section']

                    # Check section capacity (max 30 regular students)
                    existing_section_count = AppCsStudents.objects.filter(
                        program=program, 
                        year_level=year_level, 
                        section=section, 
                        status='regular'
                    ).count() + AppItStudents.objects.filter(
                        program=program, 
                        year_level=year_level, 
                        section=section, 
                        status='regular'
                    ).count()

                    if existing_section_count >= 30:
                        messages.error(request, f"Section {section} is already full (maximum 30 regular students)")
                        return render(request, 'add-students.html', {'form_data': form_data})

                # Validate section for non-regular students
                if status.lower() != 'regular':
                    if section:
                        messages.error(request, "Irregular and transferee students cannot have a section")
                        return render(request, 'add-students.html', {'form_data': form_data})
                    section = None

                # Ensure the student number is unique across both tables
                cs_student_exists = AppCsStudents.objects.filter(student_number=student_number).exists()
                it_student_exists = AppItStudents.objects.filter(student_number=student_number).exists()

                if cs_student_exists or it_student_exists:
                    messages.error(request, "Student with this student number already exists")
                    return render(request, 'add-students.html', {'form_data': form_data})

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
                        soc_fee=soc_fee,
                        address=address,
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
                        address=address,
                    )
                else:
                    # Handle other programs or raise an error
                    messages.error(request, "Invalid program selected")
                    return render(request, 'add-students.html', {'form_data': form_data})

                # Save the student object
                student_obj.save()
                messages.success(request, "Student details have been created successfully")
                return redirect('add-students')

        except IntegrityError:
            messages.error(request, "Student with this email or student number already exists")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'add-students.html', {'form_data': form_data})

    return render(request, 'add-students.html')


def MANAGE_STUDENTS(request):
    """
    View to manage students from both AppCsStudents and AppItStudents tables.
    Combines, filters, and paginates the student records.
    """
    # Fetch data from both models with a type tag
    cs_students = AppCsStudents.objects.values(
        'id', 'first_name', 'middle_name', 'last_name', 'suffix', 
        'student_number', 'program', 'year_level', 'section', 
        'email', 'mobile_number', 'status', 'soc_fee', 'date_enrolled', 'address'
    ).annotate(type=Value('CS', output_field=CharField()))
    
    it_students = AppItStudents.objects.values(
        'id', 'first_name', 'middle_name', 'last_name', 'suffix', 
        'student_number', 'program', 'year_level', 'section', 
        'email', 'mobile_number', 'status', 'soc_fee', 'date_enrolled', 'address'
    ).annotate(type=Value('IT', output_field=CharField()))

    # Combine both querysets
    combined_students = list(chain(cs_students, it_students))
    
    # Fetch program choices dynamically
    program_choices = set(
        AppCsStudents.objects.values_list('program', flat=True)
    ).union(
        AppItStudents.objects.values_list('program', flat=True)
    )

    # Convert to list of tuples for template compatibility
    program_choices = [(program, program) for program in program_choices]
    
    # Filter by selected program (if any)
    selected_program = request.GET.get('program', '').strip()
    if selected_program:
        combined_students = [
            student for student in combined_students 
            if student['program'] == selected_program
        ]
    
    # Search functionality with robust type handling
    search_query = request.GET.get('search', '').strip().lower()
    if search_query:
        combined_students = [
            student for student in combined_students 
            if (search_query in str(student['student_number']).lower() or 
                search_query in str(student['first_name']).lower() or 
                search_query in str(student['middle_name'] or '').lower() or 
                search_query in str(student['last_name']).lower())
        ]
    
    # Sort by student_number
    combined_students.sort(key=lambda x: x['student_number'])

    # Paginate results
    paginator = Paginator(combined_students, 10)  # 10 students per page
    page_number = request.GET.get('page')
    try:
        students = paginator.page(page_number)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)

    # Render context
    context = {
        'students': students,
        'program_choices': sorted(program_choices),  # Sort for better display
        'selected_program': selected_program,
    }
    return render(request, 'manage-students.html', context)


def update_students(request, student_number):
    """
    View for updating student information with student_number lookup.
    """
    # Fetch the student object using student_number
    try:
        student = AppCsStudents.objects.get(student_number=student_number)
    except AppCsStudents.DoesNotExist:
        try:
            student = AppItStudents.objects.get(student_number=student_number)
        except AppItStudents.DoesNotExist:
            raise Http404(f"Student with student_number {student_number} not found")

    # Initial context for template
    context = {
        'student': student
    }

    if request.method == "POST":
        form = StudentUpdateForm(
            request.POST,
            request.FILES,  # For file uploads
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

def enroll_students_sub(request):
    subjects = AppSub.objects.all().values(
    'sub_code', 
    'sub_name', 
    'lec_units', 
    'lab_units', 
    'year_level', 
    'semester', 
    'cs', 
    'it'
)
    return render(request, "enroll-students-sub.html", {'subjects': subjects, 'subject_range': range(1, 10)})


@csrf_protect
@require_http_methods(["POST"])
def enroll_student(request):
    try:
        # Parse the incoming JSON data
        data = json.loads(request.body)
        program = data.get('program', '')
        enrollment_data = data.get('enrollment_data', {})

        # Validate input
        student_number = enrollment_data.get('student_number')
        semester = enrollment_data.get('semester', '')  # New line to get semester
        if not student_number:
            return JsonResponse({
                'success': False, 
                'message': 'Invalid student data'
            }, status=400)

        # Determine the appropriate model based on program
        with transaction.atomic():
            if program == 'BS Computer Science':
                # Find the student
                try:
                    student = AppCsStudents.objects.get(student_number=student_number)
                    
                    # Check if student has paid SOC fee
                    if student.soc_fee != 'paid':
                        return JsonResponse({
                            'success': False, 
                            'message': 'Enrollment failed. Kindly settle your SOC fee first.'
                        }, status=403)
                    
                    # Prepare data for subject enrollment
                    subject_data = {
                        'student_number': student_number,
                        'sub1': enrollment_data.get('sub1', ''),
                        'sub2': enrollment_data.get('sub2', ''),
                        'sub3': enrollment_data.get('sub3', ''),
                        'sub4': enrollment_data.get('sub4', ''),
                        'sub5': enrollment_data.get('sub5', ''),
                        'sub6': enrollment_data.get('sub6', ''),
                        'sub7': enrollment_data.get('sub7', ''),
                        'sub8': enrollment_data.get('sub8', ''),
                        'sub9': enrollment_data.get('sub9', ''),
                        'total_units': enrollment_data.get('total_units', 0),
                        'semester': semester  # Add semester to the subject data
                    }
                    
                    # Create new subject enrollment
                    subject_enrollment = AppCsStudentsSub.objects.create(**subject_data)
                    
                    # Update enrollment date
                    student.date_enrolled = now().date()
                    student.save()
                
                except AppCsStudents.DoesNotExist:
                    return JsonResponse({
                        'success': False, 
                        'message': 'Student not found in CS program'
                    }, status=404)
            
            elif program == 'BS Information Technology':
                # Find the student
                try:
                    student = AppItStudents.objects.get(student_number=student_number)
                    
                    # Check if student has paid SOC fee
                    if student.soc_fee != 'paid':
                        return JsonResponse({
                            'success': False, 
                            'message': 'Enrollment failed. Kindly settle your SOC fee first.'
                        }, status=403)
                    
                    # Prepare data for subject enrollment
                    subject_data = {
                        'student_number': student_number,
                        'sub1': enrollment_data.get('sub1', ''),
                        'sub2': enrollment_data.get('sub2', ''),
                        'sub3': enrollment_data.get('sub3', ''),
                        'sub4': enrollment_data.get('sub4', ''),
                        'sub5': enrollment_data.get('sub5', ''),
                        'sub6': enrollment_data.get('sub6', ''),
                        'sub7': enrollment_data.get('sub7', ''),
                        'sub8': enrollment_data.get('sub8', ''),
                        'sub9': enrollment_data.get('sub9', ''),
                        'total_units': enrollment_data.get('total_units', 0),
                        'semester': semester  # Add semester to the subject data
                    }
                    
                    # Create new subject enrollment
                    subject_enrollment = AppItStudentsSub.objects.create(**subject_data)
                    
                    # Update enrollment date
                    student.date_enrolled = now().date()
                    student.save()
                
                except AppItStudents.DoesNotExist:
                    return JsonResponse({
                        'success': False, 
                        'message': 'Student not found in IT program'
                    }, status=404)
            
            else:
                return JsonResponse({
                    'success': False, 
                    'message': 'Invalid program selected'
                }, status=400)

        return JsonResponse({
            'success': True, 
            'message': 'Enrollment successful',
            'enrollment_date': student.date_enrolled.strftime('%Y-%m-%d')
        })

    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': str(e)
        }, status=500)
        
        
def manage_students_sub(request, program, student_number):
    # Determine which model to use based on the program
    if program == 'BS Computer Science':
        StudentModel = AppCsStudents
        SubjectModel = AppCsStudentsSub
    elif program == 'BS Information Technology':
        StudentModel = AppItStudents
        SubjectModel = AppItStudentsSub
    else:
        messages.error(request, 'Invalid program selected')
        return redirect('manage-students')

    # Fetch the student
    try:
        student = StudentModel.objects.get(student_number=student_number)
    except StudentModel.DoesNotExist:
        messages.error(request, 'Student not found')
        return redirect('manage-students')

    # Check if student is enrolled
    if not student.date_enrolled or student.date_enrolled == 'None':
        messages.warning(request, 'Cannot edit subjects for an unenrolled student')
        return redirect('manage-students')

    # Fetch existing subjects
    existing_subjects = SubjectModel.objects.filter(student_number=student_number).first()
    existing_subject_list = [
        getattr(existing_subjects, f'sub{i}', '') for i in range(1, 10)
    ] if existing_subjects else []
    
    # Map existing subjects to their indices
    existing_subjects_mapped = {
        i: existing_subject_list[i - 1] if i <= len(existing_subject_list) else ''
        for i in range(1, 10)
    }

    # Get all available subjects
    all_subjects =  AppSub.objects.all()

    # Prepare context
    context = {
        'existing_student': student,
        'program_type': 'CS' if program == 'BS Computer Science' else 'IT',
        'existing_subjects_mapped': existing_subjects_mapped,
        'subjects': all_subjects,
        'max_subject_slots': 9,
        'subject_range': range(1, 10),
        'page_title': f'Update Subjects for {student.first_name} {student.last_name}'
    }

    return render(request, 'manage-students-sub.html', context)

@csrf_protect
@require_http_methods(["GET"])
def get_student_subjects(request, student_number):
    """
    Retrieve student subjects based on student number and program
    """
    try:
        # First, check if the student exists in CS program
        try:
            cs_student = AppCsStudents.objects.get(student_number=student_number)
            program = 'BS Computer Science'
            
            # Try to get subjects from CS students subjects table
            try:
                student_subjects = AppCsStudentsSub.objects.get(student_number=student_number)
            except AppCsStudentsSub.DoesNotExist:
                return JsonResponse({
                    'success': False, 
                    'message': 'No subjects found for this student in CS program'
                }, status=404)
        
        except AppCsStudents.DoesNotExist:
            # If not in CS, check IT program
            try:
                it_student = AppItStudents.objects.get(student_number=student_number)
                program = 'BS Information Technology'
                
                # Try to get subjects from IT students subjects table
                try:
                    student_subjects = AppItStudentsSub.objects.get(student_number=student_number)
                except AppItStudentsSub.DoesNotExist:
                    return JsonResponse({
                        'success': False, 
                        'message': 'No subjects found for this student in IT program'
                    }, status=404)
            
            except AppItStudents.DoesNotExist:
                return JsonResponse({
                    'success': False, 
                    'message': 'Student not found in any program'
                }, status=404)

        # Prepare response data
        response_data = {
            'success': True,
            'program': program,
            'student_number': student_number,
            'total_units': student_subjects.total_units,
            'sub1': student_subjects.sub1,
            'sub2': student_subjects.sub2,
            'sub3': student_subjects.sub3,
            'sub4': student_subjects.sub4,
            'sub5': student_subjects.sub5,
            'sub6': student_subjects.sub6,
            'sub7': student_subjects.sub7,
            'sub8': student_subjects.sub8,
            'sub9': student_subjects.sub9
        }

        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': str(e)
        }, status=500)

@csrf_protect
@require_http_methods(["POST"])
def update_student_subject(request):
    """
    Update a specific subject for a student
    """
    try:
        # Parse the incoming JSON data
        data = json.loads(request.body)
        student_number = data.get('student_number')
        subject_index = data.get('subject_index')
        new_subject = data.get('new_subject')
        program = data.get('program')

        # Validate input
        if not all([student_number, new_subject, program]):
            return JsonResponse({
                'success': False, 
                'message': 'Invalid input data'
            }, status=400)

        # Determine the appropriate model based on program
        with transaction.atomic():
            if program == 'BS Computer Science':
                try:
                    # Find existing student subjects
                    student_subjects = AppCsStudentsSub.objects.get(student_number=student_number)
                    
                    # Update the specific subject dynamically
                    subject_field = f'sub{subject_index + 1}'
                    setattr(student_subjects, subject_field, new_subject)
                    student_subjects.save()
                
                except AppCsStudentsSub.DoesNotExist:
                    return JsonResponse({
                        'success': False, 
                        'message': 'Student subjects not found in CS program'
                    }, status=404)
            
            elif program == 'BS Information Technology':
                try:
                    # Find existing student subjects
                    student_subjects = AppItStudentsSub.objects.get(student_number=student_number)
                    
                    # Update the specific subject dynamically
                    subject_field = f'sub{subject_index + 1}'
                    setattr(student_subjects, subject_field, new_subject)
                    student_subjects.save()
                
                except AppItStudentsSub.DoesNotExist:
                    return JsonResponse({
                        'success': False, 
                        'message': 'Student subjects not found in IT program'
                    }, status=404)
            
            else:
                return JsonResponse({
                    'success': False, 
                    'message': 'Invalid program selected'
                }, status=400)

        return JsonResponse({
            'success': True, 
            'message': 'Subject updated successfully'
        })

    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': str(e)
        }, status=500)


def not_enrolled(request):
    """
    View to manage not enrolled students from both AppCsStudents and AppItStudents tables.
    Combines, filters, and paginates the student records that are not enrolled.
    """
    # Fetch data from both models with a type tag, filtering out enrolled students
    cs_students = AppCsStudents.objects.filter(date_enrolled__isnull=True).values(
        'id', 'first_name', 'middle_name', 'last_name', 'suffix', 
        'student_number', 'program', 'year_level', 'section',
        'email', 'mobile_number', 'status', 'soc_fee', 'date_enrolled'
    ).annotate(type=Value('CS', output_field=CharField()))
    
    it_students = AppItStudents.objects.filter(date_enrolled__isnull=True).values(
        'id', 'first_name', 'middle_name', 'last_name', 'suffix', 
        'student_number', 'program', 'year_level', 'section',
        'email', 'mobile_number', 'status', 'soc_fee', 'date_enrolled'
    ).annotate(type=Value('IT', output_field=CharField()))
    
    # Combine both querysets
    combined_students = list(chain(cs_students, it_students))
    
    # Fetch program choices dynamically for not enrolled students
    program_choices = set(
        list(AppCsStudents.objects.filter(date_enrolled__isnull=True).values_list('program', flat=True)) +
        list(AppItStudents.objects.filter(date_enrolled__isnull=True).values_list('program', flat=True))
    )
    
    # Convert to list of tuples for template compatibility
    program_choices = [(program, program) for program in program_choices]
    
    # Filter by selected program (if any)
    selected_program = request.GET.get('program', '').strip()
    if selected_program:
        combined_students = [
            student for student in combined_students 
            if student['program'] == selected_program
        ]
    
    # Sort by student_number
    combined_students.sort(key=lambda x: x['student_number'])
    
    # Paginate results
    paginator = Paginator(combined_students, 10)  # 10 students per page
    page_number = request.GET.get('page')
    try:
        students = paginator.page(page_number)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    
    # Render context
    context = {
        'students': students,
        'program_choices': sorted(program_choices),  # Sort for better display
        'selected_program': selected_program,
    }
    return render(request, 'not-enrolled.html', context)

def enrolled(request):
    """
    View to manage not enrolled students from both AppCsStudents and AppItStudents tables.
    Combines, filters, and paginates the student records that are not enrolled.
    """
    # Fetch data from both models with a type tag, filtering out enrolled students
    cs_students = AppCsStudents.objects.filter(date_enrolled__isnull=False).values(
        'id', 'first_name', 'middle_name', 'last_name', 'suffix', 
        'student_number', 'program', 'year_level', 'section',
        'email', 'mobile_number', 'status', 'soc_fee', 'date_enrolled'
    ).annotate(type=Value('CS', output_field=CharField()))
    
    it_students = AppItStudents.objects.filter(date_enrolled__isnull=False).values(
        'id', 'first_name', 'middle_name', 'last_name', 'suffix', 
        'student_number', 'program', 'year_level', 'section',
        'email', 'mobile_number', 'status', 'soc_fee', 'date_enrolled'
    ).annotate(type=Value('IT', output_field=CharField()))
    
    # Combine both querysets
    combined_students = list(chain(cs_students, it_students))
    
    # Fetch program choices dynamically for not enrolled students
    program_choices = set(
        list(AppCsStudents.objects.filter(date_enrolled__isnull=False).values_list('program', flat=True)) +
        list(AppItStudents.objects.filter(date_enrolled__isnull=False).values_list('program', flat=True))
    )
    
    # Convert to list of tuples for template compatibility
    program_choices = [(program, program) for program in program_choices]
    
    # Filter by selected program (if any)
    selected_program = request.GET.get('program', '').strip()
    if selected_program:
        combined_students = [
            student for student in combined_students 
            if student['program'] == selected_program
        ]
    
    # Sort by student_number
    combined_students.sort(key=lambda x: x['date_enrolled'], reverse=True)
    
    # Paginate results
    paginator = Paginator(combined_students, 10)  # 10 students per page
    page_number = request.GET.get('page')
    try:
        students = paginator.page(page_number)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    
    # Render context
    context = {
        'students': students,
        'program_choices': sorted(program_choices),  # Sort for better display
        'selected_program': selected_program,
    }
    return render(request, 'enrolled.html', context)





@login_required
def cor(request):
    """
    View to display student registration details based on authenticated user's email
    """
    try:
        # First, try to find the student in CS students
        student = AppCsStudents.objects.get(email=request.user.email)
        
        try:
            student_sub = AppCsStudentsSub.objects.get(student_number=student.student_number)
        except AppCsStudentsSub.DoesNotExist:
            # If student subjects not found, indicate not enrolled
            return render(request, 'cor.html', {'error_message': 'This student is not enrolled yet.'})
        
        program = 'cs'
        template = 'cor.html'
        
    except AppCsStudents.DoesNotExist:
        try:
            # If not in CS students, try IT students
            student = AppItStudents.objects.get(email=request.user.email)
            
            try:
                student_sub = AppItStudentsSub.objects.get(student_number=student.student_number)
            except AppItStudentsSub.DoesNotExist:
                # If student subjects not found, indicate not enrolled
                return render(request, 'cor.html', {'error_message': 'This student is not enrolled yet.'})
            
            program = 'it'
            template = 'cor.html'
        
        except AppItStudents.DoesNotExist:
            # If student not found in either model, show no student found error
            return render(request, 'cor.html', {'error_message': "There's no student found with this email."})
    
    # Prepare subjects with additional details from AppSub
    subject_details = []
    total_lec_units = 0
    total_lab_units = 0

    # List of subject fields to iterate through
    subject_fields = [
        'sub1', 'sub2', 'sub3', 'sub4', 'sub5', 
        'sub6', 'sub7', 'sub8', 'sub9'
    ]

    for subject_field in subject_fields:
        subject_code = getattr(student_sub, subject_field).strip()
        print(f"Checking for subject_code: {subject_code} in AppSub")
        
        # Try to find the subject in AppSub based on the subject code and program
        try:
            # Determine the correct filter based on program
            if program == 'cs':
                sub_details = AppSub.objects.get(sub_code=subject_code, cs='yes')
            else:
                sub_details = AppSub.objects.get(sub_code=subject_code, it='yes')
            
            subject_info = {
                'subject_code': subject_code,
                'subject_name': sub_details.sub_name,
                'course_description': sub_details.sub_name,
                'lecture_units': sub_details.lec_units,
                'lab_units': sub_details.lab_units,
                'time': 'TBA',
                'day': 'TBA',
                'room': 'TBA',
                'sched': 'TBA'
            }
            
            total_lec_units += sub_details.lec_units
            total_lab_units += sub_details.lab_units
            
            subject_details.append(subject_info)
        
        except AppSub.DoesNotExist:
            # If subject not found in AppSub, continue to next subject
            continue
    
    total_units = total_lec_units + total_lab_units
    
    semester = student_sub.semester

    # Modify student object to include semester
    setattr(student, 'semester', str(semester))
    
    # Prepare context with student and subjects
    context = {
        'student': student,
        'subjects': subject_details,
        'total_units': total_units,
        'total_lec_units': total_lec_units,
        'total_lab_units': total_lab_units
    }
    
    return render(request, template, context)



def is_admin(user):
    """
    Check if the logged-in user is a staff/admin
    """
    return user.is_staff and user.is_active

@user_passes_test(is_admin)
def search_cor(request):
    """
    Admin view for searching and displaying student registration details
    """
    # Initialize context variables
    context = {
        'student': None,
        'subjects': [],
        'total_units': 0,
        'total_lec_units': 0,
        'total_lab_units': 0
    }
    
    # Check if there's a search query
    search_query = request.GET.get('search', '').strip()
    
    # If search query is not empty, attempt to find student
    if search_query:
        # Try to find in CS students first
        student = AppCsStudents.objects.filter(
            Q(student_number=search_query) | 
            Q(email=search_query) | 
            Q(first_name__icontains=search_query) | 
            Q(last_name__icontains=search_query)
        ).first()
        
        if not student:
            # If not found in CS, try IT students
            student = AppItStudents.objects.filter(
                Q(student_number=search_query) | 
                Q(email=search_query) | 
                Q(first_name__icontains=search_query) | 
                Q(last_name__icontains=search_query)
            ).first()
        
        if not student:
            context['error'] = 'There\'s no student found'
            return render(request, 'search_cor.html', context)
        
        # Determine program based on student model
        program = 'cs' if isinstance(student, AppCsStudents) else 'it'
        
        try:
            # Get student subjects
            student_sub = (
                AppCsStudentsSub.objects.get(student_number=student.student_number) 
                if program == 'cs' 
                else AppItStudentsSub.objects.get(student_number=student.student_number)
            )
        except (AppCsStudentsSub.DoesNotExist, AppItStudentsSub.DoesNotExist):
            context['error'] = 'This student is not enrolled yet'
            return render(request, 'search_cor.html', context)
        
        # Prepare subjects with additional details from AppSub
        subject_details = []
        total_lec_units = 0
        total_lab_units = 0

        # List of subject fields to iterate through
        subject_fields = [
            'sub1', 'sub2', 'sub3', 'sub4', 'sub5', 
            'sub6', 'sub7', 'sub8', 'sub9'
        ]

        for subject_field in subject_fields:
            subject_code = getattr(student_sub, subject_field, '').strip()
            
            if not subject_code:
                continue
            
            # Try to find the subject in AppSub based on the subject code and program
            try:
                # Determine the correct filter based on program
                if program == 'cs':
                    sub_details = AppSub.objects.get(sub_code=subject_code, cs='yes')
                else:
                    sub_details = AppSub.objects.get(sub_code=subject_code, it='yes')
                
                subject_info = {
                    'subject_code': subject_code,
                    'subject_name': sub_details.sub_name,
                    'course_description': sub_details.sub_name,
                    'lecture_units': sub_details.lec_units,
                    'lab_units': sub_details.lab_units,
                    'time': 'TBA',
                    'day': 'TBA',
                    'room': 'TBA',
                    'sched': 'TBA'
                }
                
                total_lec_units += sub_details.lec_units
                total_lab_units += sub_details.lab_units
                
                subject_details.append(subject_info)
            
            except AppSub.DoesNotExist:
                # If subject not found in AppSub, skip
                continue
        
        total_units = total_lec_units + total_lab_units
        
        semester = student_sub.semester

        # Modify student object to include semester
        setattr(student, 'semester', str(semester))
        
        # Update context
        context = {
            'student': student,
            'subjects': subject_details,
            'total_units': total_units,
            'total_lec_units': total_lec_units,
            'total_lab_units': total_lab_units
        }
    
    return render(request, 'search_cor.html', context)



def checklist(request):
    return render(request, "checklist.html")



def sections(request):
    # Total student counts
    cs_student_count = AppCsStudents.objects.count()
    it_student_count = AppItStudents.objects.count()
    
    # Enrollment and student type statistics
    cs_enrolled_students = AppCsStudents.objects.filter(status='regular').count()
    it_enrolled_students = AppItStudents.objects.filter(status='regular').count()
    
    # Detailed enrollment breakdown by department and year level
    cs_enrollment_breakdown = (
        AppCsStudents.objects.values('year_level', 'section')
        .annotate(
            student_count=Count('id')
        )
        .order_by('year_level', 'section')
    )
    
    it_enrollment_breakdown = (
        AppItStudents.objects.values('year_level', 'section')
        .annotate(
            student_count=Count('id')
        )
        .order_by('year_level', 'section')
    )
    
    # Student status breakdown
    cs_status_breakdown = (
        AppCsStudents.objects.values('status')
        .annotate(
            student_count=Count('id')
        )
    )
    
    it_status_breakdown = (
        AppItStudents.objects.values('status')
        .annotate(
            student_count=Count('id')
        )
    )
    
    context = {
        'cs_student_count': cs_student_count,
        'it_student_count': it_student_count,
        'cs_enrolled_students': cs_enrolled_students,
        'it_enrolled_students': it_enrolled_students,
        'cs_enrollment_breakdown': cs_enrollment_breakdown,
        'it_enrollment_breakdown': it_enrollment_breakdown,
        'cs_status_breakdown': cs_status_breakdown,
        'it_status_breakdown': it_status_breakdown,
    }
    
    return render(request, 'sections.html', context)

