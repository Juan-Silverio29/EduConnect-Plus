# auth_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from .models import PerfilUsuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


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
            user = User.objects.get(pk=user.pk)
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
        institucion = request.POST.get("institucion")

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden")
            return redirect("register")

        if rol not in ["estudiante", "profesor"]:
            messages.error(request, "No puedes registrar un administrador")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe")
            return redirect("register")

        # 🔹 Crear usuario con flags correctos desde el inicio
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=nombre,
            last_name=apellido,
            is_superuser=False,
            is_staff=True if rol == "profesor" else False
        )

        # 🔹 Crear el perfil asociado
        PerfilUsuario.objects.create(
            user=user,
            institucion=institucion
        )

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
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password1 = data.get("password1", "").strip()
    password2 = data.get("password2", "").strip()
    rol = data.get("rol", "").strip()
    nombre_completo = data.get("nombre_completo", "").strip()
    alias = (data.get("alias") or "").strip() or None
    institucion = data.get("institucion", "").strip()
    semestre = data.get("semestre", "").strip() if rol == "estudiante" else None

    #  Validaciones básicas
    if not username or not email or not password1 or not password2 or not nombre_completo:
        return Response({'error': 'Por favor completa todos los campos obligatorios.'}, status=400)

    if password1 != password2:
        return Response({'error': 'Las contraseñas no coinciden.'}, status=400)

    if rol not in ["estudiante", "profesor"]:
        return Response({'error': 'Rol no válido.'}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'El usuario ya existe.'}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'El correo electrónico ya está registrado.'}, status=400)

    # Dividir nombre completo en nombre y apellido
    partes = nombre_completo.split(" ", 1)
    first_name = partes[0] if partes else ""
    last_name = partes[1] if len(partes) > 1 else ""

    # Crear usuario
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password1,
        first_name=first_name,
        last_name=last_name
    )

        # ✅ Crear el perfil automáticamente
    PerfilUsuario.objects.create(
        user=user,
        institucion=institucion,
        foto_perfil="img/default_user.png"  # si no sube una
    )

    # Asignar roles según tipo
    if rol == "profesor":
        user.is_staff = True
    else:
        user.is_staff = False
    user.is_superuser = False
    user.save()

    # Autenticación y tokens
    login(request, user)
    refresh = RefreshToken.for_user(user)

    return Response({
        'message': 'Usuario registrado exitosamente.',
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'rol': rol,
        'usuario': username
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

@login_required
def configuracion_view(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)
    return render(request, "configuracion.html", {"perfil": perfil})

class EditarPerfilForm(forms.ModelForm):
    username = forms.CharField(label="Usuario", max_length=150, required=False, disabled=True)
    first_name = forms.CharField(label="Nombre", max_length=150, required=False)
    last_name = forms.CharField(label="Apellido", max_length=150, required=False)

    class Meta:
        model = PerfilUsuario
        fields = ['foto_perfil']  # 👈 Solo este campo viene del modelo PerfilUsuario

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        # Inicializa con los datos del usuario
        self.fields['username'].initial = user.username
        self.fields['first_name'].initial = user.first_name
        self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        perfil = super().save(commit=False)
        user = perfil.user
        # Actualiza los datos del modelo User
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        if commit:
            user.save()
            perfil.save()
        return perfil


@login_required
def editar_perfil_view(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, request.FILES, instance=perfil, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Perfil actualizado correctamente.")

            # 🔹 Redirección según el tipo de usuario
            if request.user.is_superuser:
                return redirect('admin_dashboard')
            elif request.user.is_staff:
                return redirect('configuracion_profesor')  # 🔹 profesor
            else:
                return redirect('configuracion')  # 🔹 estudiante
    else:
        form = EditarPerfilForm(instance=perfil, user=request.user)

    return render(request, "editar_perfil.html", {"form": form})




@login_required
def eliminar_cuenta(request):
    """Elimina la cuenta del usuario logueado y muestra pantalla de confirmación"""
    user = request.user
    logout(request)
    user.delete()
    return render(request, 'eliminacion_exitosa.html')

@login_required
def configuracion_profesor_view(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(user=request.user)

    if not request.user.is_staff:
        messages.warning(request, "Acceso restringido a profesores.")
        return redirect("dashboard_user")

    context = {"perfil": perfil}
    return render(request, "configuracion_profesor.html", context)

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'

    def get_success_url(self):
        user = self.request.user
        # 🔹 Redirección según el tipo de usuario
        if user.is_superuser:
            return reverse_lazy('admin_dashboard')
        elif user.is_staff:
            return reverse_lazy('configuracion_profesor')
        else:
            return reverse_lazy('configuracion')