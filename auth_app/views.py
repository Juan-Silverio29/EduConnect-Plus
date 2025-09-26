#auth_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Login
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")  # 👈 cambia a la vista de tu dashboard
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

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return render(request, "register.html")

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect("dashboard")  # 👈 cambia a la vista de tu dashboard

    return render(request, "register.html")


# Logout
def logout_view(request):
    logout(request)
    return redirect("login")
# core/settings.py
#   core/settings.py    