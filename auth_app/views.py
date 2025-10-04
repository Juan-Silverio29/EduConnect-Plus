#auth_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Login
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 🚀 Redirige según el tipo de usuario
            if user.is_superuser:
                return redirect("dashboard")  # admin
            elif user.is_staff:
                return redirect("dashboard_profesor")  # profesor
            else:
                return redirect("dashboard")  # usuario normal
    return render(request, "login.html")

# Registro

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        rol = request.POST.get("rol")  # 👈 recogemos el campo rol del formulario

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect("register")

        # Crear usuario
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # Autenticar e iniciar sesión automáticamente
        user = authenticate(username=username, password=password1)
        if user is not None:
            login(request, user)          
            # Redirigir según el rol
            if rol == "profesor":
                return redirect("dashboard_profesor")
            elif rol == "mentor":
                return redirect("dashboard_mentor")
            else:  # estudiante por defecto
                return redirect("dashboard_user")

    return render(request, "register.html")


# Logout
def logout_view(request):
    logout(request)
    return redirect("login")
# core/settings.py
#   core/settings.py    