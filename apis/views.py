from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework.status import ( HTTP_400_BAD_REQUEST,
                                    HTTP_404_NOT_FOUND,
                                    HTTP_200_OK)
import json
from django.core import serializers
from django.http import HttpResponse
from django.db import IntegrityError
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import authentication_classes, permission_classes

'''
endpoint /register/student creates a user and put it in the "Students" group
'''
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def student_register(request):

    password = request.data.get("password")
    email = request.data.get("email")
    name=request.data.get('name')

    try:
        first_name = name.split()[0]
        last_name = name.split()[1]
    except:
        return Response('please enter your full name' )


    if email is None or password is None or name is None:
	       return Response({'error': 'Please provide name, email and password '},
                                                                status=HTTP_400_BAD_REQUEST)

    try:
        student = User.objects.create_user(first_name=first_name, last_name=last_name,
                                           password=password, email=email,username=email)
        student.save()
    except:
        return Response({'error': 'User with given email already exists'},status=HTTP_400_BAD_REQUEST)

    group, created = Group.objects.get_or_create(name='Students')
    #ct = ContentType.objects.get_for_model(User)
    #permission = Permission.objects.get(name='Can view user')
    #group.permissions.add(permission)
    student.groups.add(group)

    return Response(
		{
			'msg': 'Student registered successfully',

		},
        status=HTTP_200_OK)

'''
endpoint /register/teacher creates a user and put it in the "Teachers" group
'''
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def teacher_register(request):

    password = request.data.get("password")
    email = request.data.get("email")
    name=request.data.get('name')
    try:
        first_name = name.split()[0]
        last_name = name.split()[1]
    except:
        return Response('please enter your full name' )

    if email is None or password is None or name is None:
	       return Response({'error': 'Please provide name, email and password '},
                                                                status=HTTP_400_BAD_REQUEST)

    try:
        teacher = User.objects.create_user(first_name=first_name, last_name=last_name,
                                            password=password,username=email, email=email)
        teacher.save()
    except:
        return Response({'error': 'User with given email already exists'},status=HTTP_400_BAD_REQUEST)

    group, created = Group.objects.get_or_create(name='Teachers')
    #ct = ContentType.objects.get_for_model(User)
    #permission = Permission.objects.create(name = ['Can add students','can view students'],content_type=ct)
    #group.permissions.add(permission)
    teacher.groups.add(group)

    return Response(
		{
			'msg': 'Teacher account created successfully',

		},
        status=HTTP_200_OK)

'''
endpoint /register/admin creates a user and put it in the "Administrator" group
'''
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def admin_register(request):

    password = request.data.get("password")
    email = request.data.get("email")
    name=request.data.get('name')
    try:
        first_name = name.split()[0]
        last_name = name.split()[1]
    except:
        return Response('please enter your full name' )

    if email is None or password is None:
	       return Response({'error': 'Please provide name, email and password '},
                                                                status=HTTP_400_BAD_REQUEST)
    try:
        admin = User.objects.create_user(first_name=first_name, last_name=last_name,
                                         password=password,username=email, email=email)
        admin.save()
    except:
        return Response({'error': 'User with given email already exists'},status=HTTP_400_BAD_REQUEST)

    group, created = Group.objects.get_or_create(name='Administrator')
    admin.groups.add(group)



    return Response(
		{
			'msg': 'Admin created successfully',

		},
        status=HTTP_200_OK)


'''
returns access token which is used to authenricate a user
'''
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({'error': 'Please provide both email and password'},
			status=HTTP_400_BAD_REQUEST)

    user = authenticate(username=email, password=password)

    if not user:
        return Response({'error':'Please check your email and password'},
			status=HTTP_404_NOT_FOUND)

    token = get_tokens_for_user(user)

    return Response(
		{
			'token': token,
		}, status=HTTP_200_OK)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh' : str(refresh),
        'access' : str(refresh.access_token),
    }


@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def get_all_students(request):

    teachers_list = Group.objects.get(name="Teachers").user_set.all()
    admin_list = Group.objects.get(name="Administrator").user_set.all()

    if request.user in teachers_list or request.user in admin_list:
        students = list(User.objects.filter(groups__name='Students'))
        students_json = serializers.serialize('json', students)
        return HttpResponse(students_json, content_type='application/json')

    else:
        return Response('You are not authorized to perform this action')

@csrf_exempt
@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def add_students(request):
    teachers_list = Group.objects.get(name="Teachers").user_set.all()
    admin_list = Group.objects.get(name="Administrator").user_set.all()

    if request.user in teachers_list or request.user in admin_list:
        email = request.data.get("email")
        try:
            User.objects.create(username=email, email=email)
            return Response('Student added successfully')
        except:
            return Response('User with this email already exists')
    else:
        return Response('You are not authorized to perform this action')

@csrf_exempt
@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def view_student_profile(request):
    if request.user.groups.filter(name = 'Students').exists():
        first_name=request.user.first_name
        last_name=request.user.last_name
        email=request.user.email

        return Response({'First name': first_name, 'Last name': last_name, 'Email':email})
    else:
        return Response('Only a student can view his/her profile')
