from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse

# class CustomLogoutView(LogoutView):
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)

def success_view(request):
    return HttpResponse("Enrollment successful!")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('base4/',views.base4,name="base4"),
    path('home/',views.home,name="home"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('add-students/',views.ADD_STUDENT,name="add-students"),
    path('manage-students/', views.MANAGE_STUDENTS, name='manage-students'),
    path('update-students/<str:student_number>/', views.update_students, name='update-students'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('enroll-students-sub/',views.enroll_students_sub,name="enroll-students-sub"),
    path('enroll_student/', views.enroll_student, name='enroll_student'),
    path('get_student_subjects/<int:student_number>/', views.get_student_subjects, name='get_student_subjects'),
    path('manage-students-sub/<str:program>/<str:student_number>/', views.manage_students_sub, name='manage-students-sub'),
    path('update_student_subject/', views.update_student_subject, name='update_student_subject'),
    path('not-enrolled/', views.not_enrolled, name='not-enrolled'),
    path('enrolled/', views.enrolled, name='enrolled'),
    path('dashboard1/',views.dashboard1,name="dashboard1"),
    path('checklist/',views.checklist,name="checklist"),
    path('register/',views.register,name="register"),
    path('profile/', views.profile, name='profile'),
    path('', auth_view.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', views.logout_view, name='logout'),

]
