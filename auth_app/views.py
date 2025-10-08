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
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # 🚀 Redirigir según rol
            if user.is_superuser:
                return redirect("dashboard_user")       # o un dashboard admin
            elif user.is_staff:  # Profesor
                return redirect("dashboard_profesor")
            else:  # Alumno normal
                return redirect("dashboard_user")
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, "login.html")

# Registro

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        rol = request.POST.get("rol")  # 👈 se obtiene el rol del formulario

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect("register")

        # Crear usuario
        user = User.objects.create_user(username=username, email=email, password=password1)

        # 👩‍🏫 Si es profesor → marcarlo como staff
        if rol == "profesor":
            user.is_staff = True
            user.save()

        # 👨‍🎓 Si es mentor → lo podrías marcar con un grupo o permiso especial (opcional)
        if rol == "mentor":
            
            pass

        # Iniciar sesión automáticamente
        login(request, user)

        # Redirigir según rol
        if rol == "profesor":
            return redirect("dashboard_profesor")
        else:
            return redirect("dashboard_user")

    return render(request, "register.html")



# Logout
def logout_view(request):
    logout(request)
    return redirect("login")
# core/settings.py
#   core/settings.py    