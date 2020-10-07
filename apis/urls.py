from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'apis'

urlpatterns = [
    path('register/student', views.student_register),
    path('register/teacher', views.teacher_register),
    path('register/admin', views.admin_register),
    path('login', views.login, name='login'),
    path('students', views.get_all_students),
    path('add-student', views.add_students),
    path('student-profile', views.view_student_profile)
]
