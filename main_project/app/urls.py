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
    path('update-students/<int:student_id>/', views.update_students, name='update-students'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('dashboard1/',views.dashboard1,name="dashboard1"),
    path('checklist/',views.checklist,name="checklist"),
    path('enroll/',views.enroll,name="enroll"),
    path('register/',views.register,name="register"),
    path('profile/', views.profile, name='profile'),
    path('', auth_view.LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', views.logout_view, name='logout'),

]
