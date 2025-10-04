#landing/views.py
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

def home(request):
    return render(request, 'landing.html')

# Vista protegida (API)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_info(request):
    """
    Esta vista solo es accesible si el usuario ha iniciado sesión
    y manda un JWT válido en el encabezado Authorization.
    """
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
        "message": "Bienvenido a la API protegida"
    })


@api_view(['POST'])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'username' : str(username),
            'password' : str(password),
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Usuario o contraseña incorrectos'}, status=status.HTTP_401_UNAUTHORIZED)
