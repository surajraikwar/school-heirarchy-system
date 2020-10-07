from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'apis'

urlpatterns = [
    path('register/student', views.student_register),
    path('register/teacher', views.teacher_register),
    path('register/admin', views.admin_register),
    path('login', views.login, name='login'),
    path('', views.list_all_users),            #admin can view all the users in the database
    path('add-user', views.add_user),           #admin can add students, teachers and other admins as well
    path('students', views.get_all_students),   #teachers and admins can get list of all students in the database
    path('add-student', views.add_students),    #teachers and admins can add students
    path('student-profile', views.view_student_profile)     #only students can view their profile
]
