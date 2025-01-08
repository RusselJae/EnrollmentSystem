from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_view
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse


urlpatterns = [
    path('admin/', admin.site.urls),
    path('base4/',views.base4,name="base4"),
    path('home/',views.home,name='home'),
    path('add-students/',views.add_students,name="add-students"),
    path('manage-students/', views.manage_students, name='manage-students'),
    path('archive/', views.archive, name='archive'),
    path('update-students/<str:student_number>/', views.update_students, name='update-students'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('enroll-students-sub/',views.enroll_students_sub,name="enroll-students-sub"),
    path('enroll_student/', views.enroll_student, name='enroll_student'),
    path('get_student_subjects/<int:student_number>/', views.get_student_subjects, name='get_student_subjects'),
    path('manage-students-sub/<str:program>/<str:student_number>/', views.manage_students_sub, name='manage-students-sub'),
    path('update_student_subject/', views.update_student_subject, name='update_student_subject'),
    path('not-enrolled/', views.not_enrolled, name='not-enrolled'),
    path('enrolled/', views.enrolled, name='enrolled'),
    path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('checklist/',views.checklist,name="checklist"),
    path('register/',views.register,name="register"),
    path('profile/', views.profile, name='profile'),
    # path('', auth_view.LoginView.as_view(template_name='login.html'), name="login"),
    path('doLogout/', views.doLogout, name='logout'),
    path('', views.LoginView.as_view(), name='login'),
    path('cor/', views.cor, name='cor'),
    path('search_cor/', views.search_cor, name='search_cor'),
    path('sections/', views.sections, name='sections'),
    path('admin-profile/', views.admin_profile_update, name='admin_profile'),
    path('student-profile/', views.student_profile, name='student_profile'),
    path('archive_student/<str:program><int:student_id>/', views.archive_student, name='archive_student'),
    path('restore_student/<str:program><int:student_id>/', views.restore_student, name='restore_student'),
    
    path('password-reset/', 
         auth_view.PasswordResetView.as_view(template_name='password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), 
         name='password_reset_complete'),
]
