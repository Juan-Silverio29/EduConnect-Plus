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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # iniciar sesión automáticamente
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


# Logout
def logout_view(request):
    logout(request)
    return redirect("login")
# core/settings.py
#   core/settings.py    