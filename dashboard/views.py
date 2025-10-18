# dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from resources.models import Recursos
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import MaterialDidactico
from .forms import MaterialForm
from django.shortcuts import render, redirect
from auth_app.models import PerfilUsuario 
from django.contrib import messages

# ---------------------------
# Prueba JWT
# ---------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def prueba_jwt(request):
    return Response({
        "message": f"Hola {request.user.username}, tu JWT funciona!"
    })

# ---------------------------
# Dashboards
# ---------------------------
@login_required
def dashboard_view(request):
    user = request.user

    if user.is_superuser or user.is_staff:
        return render(request, "dashboard_admin.html")

    if hasattr(user, "is_teacher") and user.is_teacher:
        cursos = [
            {"nombre": "Matemáticas I", "grupo": "1A", "alumnos": 30},
            {"nombre": "Historia", "grupo": "2B", "alumnos": 25},
        ]
        return render(request, "dashboard_profesor.html", {"cursos": cursos})

    return render(request, "dashboard_user.html")


@login_required
def dashboard_profesor(request):
    return render(request, "dashboard_profesor.html")


@login_required
def dashboard_user(request):
    return render(request, "dashboard_user.html")


# ---------------------------
# Logros y progreso de recursos
# ---------------------------
@login_required
def logros_recursos_completados(request):
    recursos = Recursos.objects.filter(completado=True)
    total_recursos = Recursos.objects.count()

    progreso = 0
    if total_recursos > 0:
        progreso = int((recursos.count() / total_recursos) * 100)

    return render(request, "logros_recursos_completados.html", {
        "recursos": recursos,
        "total_recursos": total_recursos,
        "progreso": progreso
    })


# ---------------------------
# Funciones del profesor
# ---------------------------
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
    materiales = [
        {"titulo": "Apuntes Matemáticas", "curso": "Matemáticas I"},
        {"titulo": "Libro Historia", "curso": "Historia"},
    ]
    return render(request, "profesor_material.html", {"materiales": materiales})

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
            return redirect('profesor_material')
    else:
        form = MaterialForm()

    context = {
        'materiales': materiales,
        'form': form,
    }
    return render(request, 'profesor_material.html', context)

