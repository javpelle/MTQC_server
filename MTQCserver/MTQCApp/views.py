from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from MTQCApp.commprotocol.server_response import SUCCESS, WRONG_JSON, ServerResponse

from .services import user_service
from .services import project_service

# Create your views here.


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            user_data = JSONParser().parse(request)
        except:
            return JsonResponse(ServerResponse(status=WRONG_JSON).get(), safe=False)

        client = user_service.login(user_data)
        server_response = ServerResponse()
        server_response.set_status(client["status"])
        if client["status"] == SUCCESS:
            server_response.set_data({"token": client["token"]})
        return JsonResponse(server_response.get(), safe=False)


@csrf_exempt
def guest_login(request):
    if request.method == 'GET':
        client = user_service.guest_login()
        server_response = ServerResponse(status=client["status"], data={
                                         "token": client["token"]})
        return JsonResponse(server_response.get(), safe=False)


@csrf_exempt
def verify_account(request, token):
    if request.method == 'GET':
        client = user_service.verify_account(token)
        server_response = ServerResponse(status=client["status"])
        # Aquí deberíamos devolver una web maja que diga verificado correctamente, ya puedes cerrar la ventanita
        # O en su defecto redirigir al login-page de Angular
        return JsonResponse(server_response.get(), safe=False)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            user_data = JSONParser().parse(request)
        except:
            return JsonResponse(ServerResponse(status=WRONG_JSON).get(), safe=False)

        client = user_service.register(user_data)
        server_response = ServerResponse(status=client["status"])
        if client["status"] == SUCCESS:
            server_response.set_data({"verified": client["verified"]})
        return JsonResponse(server_response.get(), safe=False)


@csrf_exempt
def change_password(request):
    if request.method == 'POST':
        try:
            user_data = JSONParser().parse(request)
        except:
            return JsonResponse(ServerResponse(status=WRONG_JSON).get(), safe=False)

        user = user_service.change_password(
            user_data, request.headers["Authorization"])
        server_response = ServerResponse(status=user["status"])
        if user["status"] == SUCCESS:
            server_response.set_data({"token": user["token"]})
        return JsonResponse(server_response.get(), safe=False)


@csrf_exempt
def new_project(request):
    if request.method == 'POST':
        try:
            project_data = JSONParser().parse(request)
        except:
            return JsonResponse(ServerResponse(status=WRONG_JSON).get(), safe=False)

        user_data = user_service.get_user_from_auth(request.headers["Authorization"])
        if user_data["status"] != SUCCESS:
            return JsonResponse(ServerResponse(status=user_data["status"]).get(), safe=False)

        user = user_data["user"]
        project = project_service.new_project(project_data, user)
        server_response = ServerResponse(status=user["status"])
        if project["status"] == SUCCESS:
            server_response.set_data({"project": user["project"]})
        return JsonResponse(server_response.get(), safe=False)



        
        
