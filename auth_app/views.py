# auth_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# DRF y JWT
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# ------------------------------
# VISTAS NORMALES (Django)
# ------------------------------

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            print(f"[DEBUG] Usuario: {user.username} | is_superuser: {user.is_superuser} | is_staff: {user.is_staff}")
            if user.is_superuser:
                return redirect("admin_dashboard")
            elif user.is_staff:
                return redirect("dashboard_profesor")
            else:
                return redirect("dashboard_user")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, "login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        rol = request.POST.get("rol")
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect("register")

        if rol not in ["estudiante", "profesor"]:
            messages.error(request, "No puedes registrar un administrador")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=nombre,
            last_name=apellido
        )

        # Asignar roles correctamente
        if rol == "profesor":
            user.is_staff = True
        else:
            user.is_staff = False
        user.is_superuser = False  # nunca un profesor es superuser
        user.save()

        login(request, user)

        if rol == "profesor":
            return redirect("dashboard_profesor")
        else:
            return redirect("dashboard_user")

    return render(request, "register.html")


def logout_view(request):
    logout(request)
    return redirect("login")


# ------------------------------
# VISTAS API (DRF + JWT)
# ------------------------------

@api_view(['POST'])
def api_login(request):
    """
    Login vía API, devuelve access y refresh JWT.
    """
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })
    return Response({'error': 'Usuario o contraseña incorrectos'}, status=400)


@api_view(['POST'])
def api_register(request):
    """
    Registro vía API, devuelve JWT.
    """
    username = request.data.get("username")
    email = request.data.get("email")
    password1 = request.data.get("password1")
    password2 = request.data.get("password2")
    rol = request.data.get("rol")
    nombre = request.data.get("nombre")
    apellido = request.data.get("apellido")

    if password1 != password2:
        return Response({'error': 'Las contraseñas no coinciden'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'El usuario ya existe'}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password1,
        first_name=nombre,
        last_name=apellido
    )

    if rol == "profesor":
        user.is_staff = True
        user.save()

    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'rol': rol
    }, status=201)


# 🔹 NUEVOS endpoints con sesión Django

@api_view(['POST'])
def api_register_session(request):
    data = request.data
    username = data.get("username")
    email = data.get("email")
    password1 = data.get("password1")
    password2 = data.get("password2")
    rol = data.get("rol")
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    fecha_nacimiento = data.get("fecha_nacimiento")
    telefono = data.get("telefono")
    institucion = data.get("institucion")
    grado = data.get("grado") if rol == "estudiante" else None

    if password1 != password2:
        return Response({'error': 'Las contraseñas no coinciden'}, status=400)
    if rol not in ["estudiante", "profesor"]:
        return Response({'error': 'Rol no válido'}, status=400)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'El usuario ya existe'}, status=400)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password1,
        first_name=nombre,
        last_name=apellido
    )

    # Asignar roles
    if rol == "profesor":
        user.is_staff = False
    else:
        user.is_staff = False
    user.is_superuser = False
    user.save()

    login(request, user)
    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'rol': rol
    }, status=201)


@api_view(['POST'])
def api_login_session(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(request, username=username, password=password)

    if user:
        login(request, user)
        refresh = RefreshToken.for_user(user)

        # Determinar rol correctamente
        if user.is_superuser:
            rol = "admin"
        elif user.is_staff:
            rol = "profesor"
        else:
            rol = "estudiante"

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'rol': rol
        })

    return Response({'error': 'Usuario o contraseña incorrectos'}, status=400)

def privacy_policy_view(request):
    return render(request, "privacy.html")  # crea un archivo privacy.html

# ------------------------------
# Fin de auth_app/views.py 
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    user = request.user
    if user.is_superuser:
        return redirect('admin_dashboard')
    elif user.is_staff:
        return redirect('dashboard_profesor')
    else:
        return redirect('dashboard_user')


@login_required
def estudiante_dashboard(request):
    context = {
        "recursos": [
            {"nombre": "Curso A", "completado": True},
            {"nombre": "Curso B", "completado": False},
        ]
    }
    return render(request, "dashboard_user.html", context)


@login_required
def profesor_dashboard(request):
    cursos = [
        {"nombre": "Matemáticas I", "grupo": "1A", "alumnos": 30},
        {"nombre": "Historia", "grupo": "2B", "alumnos": 25},
    ]
    context = {
        "cursos": cursos,
        "cursos_activos": len(cursos),
        "alumnos_inscritos": sum(c['alumnos'] for c in cursos),
        "tareas_revisadas": 10,
        "material_subido": 5,
    }
    return render(request, "profesor_dashboard.html", context)


@login_required
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")
