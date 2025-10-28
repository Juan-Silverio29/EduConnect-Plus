from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse

from auth_app.models import PerfilUsuario
from forum.models import Foro
from .models import MaterialDidactico
from .forms import MaterialForm

# ---------------------------
# Redirección según el rol
# ---------------------------
@login_required
def dashboard_view(request):
    user = request.user

    if user.is_superuser or user.is_staff:
        return redirect('dashboard:dashboard_admin')
    elif hasattr(user, "perfilusuario") and getattr(user.perfilusuario, "is_teacher", False):
        return redirect('dashboard:dashboard_profesor')
    else:
        return redirect('dashboard:dashboard_user')


# ---------------------------
# DASHBOARD: ADMINISTRADOR
# ---------------------------
@login_required
def dashboard_admin(request):
    if not request.user.is_staff:
        messages.error(request, "❌ No tienes permisos para acceder al panel de administración.")
        return redirect('dashboard:dashboard_user')

    total_usuarios = User.objects.count()
    total_profesores = PerfilUsuario.objects.filter(is_teacher=True).count()
    total_cursos = 8  # temporalmente estático, puedes cambiarlo según tu modelo real

    context = {
        "total_usuarios": total_usuarios,
        "total_profesores": total_profesores,
        "total_cursos": total_cursos,
    }
    return render(request, "dashboard_admin.html", context)


'''@login_required
def admin_usuarios(request):
    usuarios = User.objects.all().select_related("perfilusuario")
    return render(request, "admin_usuarios.html", {"usuarios": usuarios})'''

def admin_usuarios(request):
    # Traemos todos los usuarios con su perfil
    usuarios = PerfilUsuario.objects.select_related('user').all()
    return render(request, "admin_usuarios.html", {"usuarios": usuarios})

'''@login_required
def admin_cursos(request):
    cursos = [
        {"nombre": "Matemáticas I", "profesor": "Juan Pérez", "alumnos": 30},
        {"nombre": "Historia Universal", "profesor": "María López", "alumnos": 25},
    ]
    return render(request, "admin_cursos.html", {"cursos": cursos})'''
@login_required
def admin_cursos(request):
    # Traemos todos los cursos
    cursos = Curso.objects.select_related('profesor').all()
    return render(request, "admin_cursos.html", {"cursos": cursos})

@login_required
def admin_estadisticas(request):
    data = {
        "usuarios": User.objects.count(),
        "profesores": PerfilUsuario.objects.filter(is_teacher=True).count(),
    }
    return render(request, "admin_estadisticas.html", data)


# ---------------------------
# DASHBOARD: PROFESOR
# ---------------------------
@login_required
def dashboard_profesor(request):
    return render(request, "dashboard_profesor.html")


@login_required
def profesor_cursos(request):
    cursos = [
        {"nombre": "Matemáticas I", "grupo": "1A", "alumnos": 30},
        {"nombre": "Historia", "grupo": "2B", "alumnos": 25},
    ]
    return render(request, "profesor_cursos.html", {"cursos": cursos})


@login_required
def profesor_evaluaciones(request):
    evaluaciones = [
        {"nombre": "Examen 1", "curso": "Matemáticas I", "fecha": "2025-10-15"},
        {"nombre": "Examen 2", "curso": "Historia", "fecha": "2025-10-20"},
    ]
    return render(request, "profesor_evaluaciones.html", {"evaluaciones": evaluaciones})


@login_required
def profesor_material(request):
    materiales = MaterialDidactico.objects.filter(profesor=request.user).order_by('-fecha')

    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.profesor = request.user
            material.save()
            messages.success(request, "✅ Material subido correctamente.")
            return redirect('dashboard:profesor_material')
    else:
        form = MaterialForm()

    return render(request, 'profesor_material.html', {'materiales': materiales, 'form': form})


@login_required
def editar_material_view(request, id):
    material = get_object_or_404(MaterialDidactico, id=id, profesor=request.user)
    if request.method == 'POST':
        material.titulo = request.POST.get('titulo')
        material.tipo = request.POST.get('tipo')
        if request.FILES.get('archivo'):
            material.archivo = request.FILES['archivo']
        material.enlace = request.POST.get('enlace')
        material.save()
        messages.success(request, "✅ Material actualizado correctamente.")
        return redirect('dashboard:profesor_material')
    return render(request, 'editar_material.html', {'material': material})


@login_required
def eliminar_material_view(request, id):
    material = get_object_or_404(MaterialDidactico, id=id, profesor=request.user)
    material.delete()
    messages.success(request, "🗑️ Material eliminado correctamente.")
    return redirect('dashboard:profesor_material')


@login_required
def foros_profesor(request):
    foros = Foro.objects.all().order_by('-fecha_creacion')
    return render(request, 'foros_profesor.html', {'foros': foros})


# ---------------------------
# DASHBOARD: USUARIO
# ---------------------------
@login_required
def dashboard_user(request):
    return render(request, "dashboard_user.html")
