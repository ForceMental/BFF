from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
import jwt
from rest_framework import status
import requests
from django.contrib.auth import authenticate
from .backends import AzureADBackend
from datetime import datetime
from .models import Usuario
EXTERNAL_HOST = "3.81.65.202"
@permission_classes([IsAuthenticated])
def view_all_users(request):
    # Recupera todos los usuarios registrados en la base de datos
    users = Usuario.objects.all()

    # Crea una lista para almacenar los datos de todos los usuarios
    user_list = []

    # Itera a través de los usuarios y agrega sus datos a la lista
    for user in users:
        user_data = {
            'user-id': user.user_id,
            'username': user.username,
            'first_name': user.first_name,
            'email': user.email,
        }
        user_list.append(user_data)

    # Devuelve la lista de usuarios en formato JSON
    return JsonResponse({'users': user_list})

@permission_classes([IsAuthenticated])
def get_user_view(request):
    # Obteniendo el token del encabezado de autorización
    auth_header = request.headers.get('Authorization')
    if not auth_header or 'Bearer ' not in auth_header:
        return HttpResponseBadRequest("Token no proporcionado o encabezado de autorización incorrecto")

    token = auth_header.split('Bearer ')[1]

    try:
        decoded_token = jwt.decode(token, verify=False)
        user_sub = decoded_token.get('sub')
        user_first_name = decoded_token.get('name')
        user_email = decoded_token.get('email')

        if not user_sub:
            return HttpResponseBadRequest("Token no contiene el campo 'sub'")

        # Intenta encontrar un usuario existente con el mismo 'username' igual al 'sub'
        user, created = Usuario.objects.get_or_create(username=user_sub, defaults={
            'first_name': user_first_name,  # Asigna el valor del token a 'first_name'
            'email': user_email,            # Asigna el valor del token a 'email'
        })

        if created:
            # El usuario no existía en la base de datos, así que lo guardamos y devolvemos un mensaje de registro exitoso
            return JsonResponse({
                'user-id': user.user_id,  # Utiliza el campo autoincrementable 'user_id'
                'username': user.username,
                'first_name': user.first_name,
                'email': user.email,
                'message': 'Usuario registrado exitosamente',
            })
        else:
            # El usuario ya existía en la base de datos, así que devolvemos sus datos
            return JsonResponse({
                'user-id': user.user_id,
                'username': user.username,
                'first_name': user.first_name,
                'email': user.email,
                'message': 'Usuario encontrado',
            })

    except jwt.DecodeError:
        return HttpResponseBadRequest("Error al decodificar el token")

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_comunas(request):
    API_URL = f"http://{EXTERNAL_HOST}:8000/api/comunas/"
    response = requests.get(API_URL)
    return Response(response.json())

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_client(request):
    API_URL = f"http://{EXTERNAL_HOST}:8000/api/clientes/"
    response = requests.get(API_URL)
    return Response(response.json())


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def insertar_persona(request):
    data = request.data
    nombre = data.get('nombre', None)
    apellido = data.get('apellido', None)
    telefono = data.get('telefono', None)
    correo_electronico = data.get('correo_electronico', None)
    direccion = data.get('direccion', None)
    rut = data.get('rut', None)
    comuna = data.get('comuna', None)

    if not nombre or not apellido or not telefono or not correo_electronico or not direccion or not rut or comuna is None:
        return Response({"error": "Datos incompletos"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        external_url = f"http://{EXTERNAL_HOST}:8000/api/clientes/create/"

        data_to_send = {
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono,
            "correo_electronico": correo_electronico,
            "direccion": direccion,
            "rut": rut,
            "comuna": comuna,
        }
        
        response = requests.post(external_url, json=data_to_send,  timeout=10)
        
        if 200 <= response.status_code < 300:
            return Response(response.json(), status=response.status_code)
        else:
            return Response({"error": "Error al comunicarse con el servicio externo", "external_status": response.status_code}, status=status.HTTP_502_BAD_GATEWAY)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_product(request):
    API_URL = f"http://{EXTERNAL_HOST}:8020/api/productos/"
    response = requests.get(API_URL)
    return Response(response.json())

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_visitas_by_date(request, fecha):
    try:
        # Convierte la fecha de "dd-mm-yyyy" a un objeto datetime
        date_obj = datetime.strptime(fecha, '%d-%m-%Y')

        # Formatea la fecha en el formato deseado
        fecha_formateada = date_obj.strftime('%d-%m-%Y')
        print (fecha_formateada)
        # URL de la API externa
        API_URL = f"http://{EXTERNAL_HOST}:8000/api/visitas/{fecha_formateada}"

        # Realiza una solicitud GET a la API externa
        response = requests.get(API_URL)

        # Verifica si la solicitud fue exitosa (código de respuesta 200)
        if response.status_code == 200:
            visitas = response.json()
            return Response(visitas)
        else:
            return Response({'error': 'Error al obtener las visitas'}, status=response.status_code)

    except Exception as e:
        return Response({'error': 'Error al procesar la solicitud'}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_visita(request):
    data = request.data
    tipo_visita = data.get('tipo_visita', None)
    cliente_id = data.get('cliente_id', None)
    empleado_id = data.get('empleado_id', None)
    fecha_visita = data.get('fecha_visita', None)

    if (
        tipo_visita is None
        or cliente_id is None
        or empleado_id is None
        or fecha_visita is None
    ):
        return Response({"error": "Datos incompletos"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        external_url = f"http://{EXTERNAL_HOST}:8000/api/visitas/"

        data_to_send = {
            "tipo_visita": tipo_visita,
            "cliente_id": cliente_id,
            "empleado_id": empleado_id,
            "fecha_visita": fecha_visita,
        }

        response = requests.post(external_url, json=data_to_send, timeout=10)

        if 200 <= response.status_code < 300:
            return Response(response.json(), status=response.status_code)
        else:
            return Response(
                {
                    "error": "Error al comunicarse con el servicio externo",
                    "external_status": response.status_code,
                },
                status=status.HTTP_502_BAD_GATEWAY,
            )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)