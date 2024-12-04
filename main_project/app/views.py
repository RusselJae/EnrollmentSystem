from datetime import timezone
from itertools import chain
from django.db import IntegrityError
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import Http404, HttpResponseRedirect
from .models import AppCsStudents, AppCsStudentsSub, AppItStudents, AppItStudentsSub, AppSub
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import StudentUpdateForm 
from django.contrib import messages
from django.core.files.storage import default_storage
from django.db.models import Value, CharField, Q  # Import for annotations
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
    
    # Prepare context to pass to the template
    context = {
        'cs_student_count': cs_student_count,
        'it_student_count': it_student_count,
        'total_students': cs_student_count + it_student_count,
        'enrolled_students': enrolled_students,
        'unenrolled_students': unenrolled_students
    }
    
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
                        soc_fee=soc_fee,
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
        'email', 'mobile_number', 'status', 'soc_fee', 'date_enrolled'
    ).annotate(type=Value('CS', output_field=CharField()))
    
    it_students = AppItStudents.objects.values(
        'id', 'first_name', 'middle_name', 'last_name', 'suffix', 
        'student_number', 'program', 'year_level', 'section', 
        'email', 'mobile_number', 'status', 'soc_fee', 'date_enrolled'
    ).annotate(type=Value('IT', output_field=CharField()))

    # Combine both querysets
    combined_students = list(chain(cs_students, it_students))
    
    # Fetch program choices dynamically
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
                        'total_units': enrollment_data.get('total_units', 0)
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
                        'total_units': enrollment_data.get('total_units', 0)
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






def checklist(request):
    return render(request, "checklist.html")



