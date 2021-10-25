from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from MTQCApp.models import User
from MTQCApp.serializers import UserSerializer

# Create your views here.


@csrf_exempt
def login(request):
    if request.method == 'POST':
        userData = JSONParser().parse(request)
        try:
            user = User.objects.get(email=userData['email'])
        except User.DoesNotExist:
            user = None
        if user is not None:
            if user.password == userData['password']:
                return JsonResponse("Login Successfully!!", safe=False)
            else:
                return JsonResponse("Wrong password!!", safe=False)
        return JsonResponse("Does not exist the email", safe=False)


@csrf_exempt
def register(request):
    if request.method != 'POST':
        userData = JSONParser().parse(request)
        department_serializer = UserSerializer(data=userData)
        if department_serializer.is_valid():
            try:
                user = User.objects.get(email=userData['email'])
            except User.DoesNotExist:
                user = None
            if user is None:
                department_serializer.save()
                return JsonResponse("Added Successfully!!", safe=False)
            else:
                return JsonResponse("User already exists", safe=False)
        else:
            return JsonResponse("Bad JSON", safe=False)
