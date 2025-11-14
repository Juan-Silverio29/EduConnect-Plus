from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from datetime import date
import os
import json
import pandas as pd
import plotly.express as px
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from dashboard.models import Actividad
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse  # <-- IMPORT IMPORTANTE
from .models import Curso, Actividad, Tarea, EntregaTarea, MaterialDidactico, Inscripcion


# Modelos
from .models import (
    Curso, Inscripcion, MaterialDidactico,
    Evaluacion, UserActivity, LearningSession,
    Tarea, EntregaTarea
)

from auth_app.models import PerfilUsuario
from forum.models import Foro
from dashboard.models import UserActivity, LearningSession
from .models import Curso, Inscripcion, MaterialDidactico, Evaluacion

# Formularios
from .forms import CursoForm, MaterialForm, EvaluacionForm

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
    total_cursos = Curso.objects.count()  # Ahora dinámico
    
    context = {
        "total_usuarios": total_usuarios,
        "total_profesores": total_profesores,
        "total_cursos": total_cursos,
    }
    return render(request, "dashboard_admin.html", context)

@login_required
def admin_usuarios(request):
    usuarios = PerfilUsuario.objects.select_related('user').all()
    return render(request, "admin_usuarios.html", {"usuarios": usuarios})

@login_required
def admin_cursos(request):
    cursos = Curso.objects.select_related('profesor').all()
    return render(request, "admin_cursos.html", {"cursos": cursos})

@login_required
def admin_estadisticas(request):
    data = {
        "usuarios": User.objects.count(),
        "profesores": PerfilUsuario.objects.filter(is_teacher=True).count(),
        "cursos": Curso.objects.count(),
    }
    return render(request, "admin_estadisticas.html", data)

# ---------------------------
# DASHBOARD: PROFESOR
# ---------------------------

@login_required
def dashboard_profesor(request):
    profesor = request.user
    
    # Cursos activos creados por el profesor
    cursos_activos = Curso.objects.filter(profesor=profesor).count()
    
    # Cursos recientes para mostrar
    cursos = Curso.objects.filter(profesor=profesor).order_by('-fecha_creacion')[:4]
    
    # Alumnos inscritos en los cursos del profesor
    alumnos_inscritos = Inscripcion.objects.filter(curso__profesor=profesor).count()
    
    # Materiales subidos por el profesor
    materiales_subidos = MaterialDidactico.objects.filter(profesor=profesor).count()
    
    # Evaluaciones próximas
    evaluaciones = Evaluacion.objects.filter(
        profesor=profesor, 
        fecha__gte=date.today()
    ).order_by('fecha')[:5]
    
    # Tareas revisadas
    tareas_revisadas = 0  # Por ahora lo dejamos en 0 si aún no existe ese modelo
    
    context = {
        "cursos_activos": cursos_activos,
        "alumnos_inscritos": alumnos_inscritos,
        "tareas_revisadas": tareas_revisadas,
        "material_subido": materiales_subidos,
        "cursos": cursos,
        "evaluaciones": evaluaciones,
    }
    return render(request, "dashboard_profesor.html", context)

@login_required
def profesor_cursos(request):
    """Muestra los cursos creados por el profesor logueado."""
    cursos = Curso.objects.filter(profesor=request.user).order_by("-id")
    return render(request, "profesor_cursos.html", {"cursos": cursos})

@login_required
def profesor_evaluaciones(request):
    evaluaciones = Evaluacion.objects.filter(profesor=request.user).order_by('-fecha')
    return render(request, "profesor_evaluaciones.html", {"evaluaciones": evaluaciones})

@login_required
def profesor_material(request):
    # 🔹 Mostrar materiales del profesor
    materiales = MaterialDidactico.objects.filter(profesor=request.user).order_by('-fecha_subida')
    
    # 🔹 Traer cursos del profesor para el selector
    cursos = Curso.objects.filter(profesor=request.user)
    
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.profesor = request.user
            
            # 🔹 Asociar el curso seleccionado (si existe)
            curso_id = request.POST.get('curso')
            if curso_id:
                try:
                    material.curso = Curso.objects.get(id=curso_id, profesor=request.user)
                except Curso.DoesNotExist:
                    material.curso = None
            
            # 🔹 Detectar tipo automáticamente
            archivo = material.archivo
            if archivo:
                ext = os.path.splitext(archivo.name)[1].lower()
                if ext in ['.pdf']:
                    material.tipo = 'PDF'
                elif ext in ['.ppt', '.pptx']:
                    material.tipo = 'Presentación'
                elif ext in ['.mp4', '.mov', '.avi']:
                    material.tipo = 'Video'
                elif ext in ['.doc', '.docx']:
                    material.tipo = 'Documento'
                else:
                    material.tipo = 'Otro'
            elif material.enlace:
                material.tipo = 'Enlace'
            else:
                material.tipo = 'Otro'
            
            material.save()
            messages.success(request, "✅ Material subido correctamente.")
            return redirect('dashboard:profesor_material')
    else:
        form = MaterialForm()
    
    return render(request, 'profesor_material.html', {
        'form': form,
        'materiales': materiales,
        'cursos': cursos
    })

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
# DASHBOARD: USUARIO (ALUMNO)
# ---------------------------

@login_required
def dashboard_user(request):
    """Vista principal del dashboard para estudiantes con datos dinámicos"""
    alumno = request.user
    
    try:
        # Cursos en los que está inscrito
        cursos_inscritos = Inscripcion.objects.filter(alumno=alumno, activa=True)
        user_cursos_count = cursos_inscritos.count()
        
        # Recursos totales de esos cursos
        cursos_ids = cursos_inscritos.values_list('curso', flat=True)
        recursos = MaterialDidactico.objects.filter(curso__in=cursos_ids, visible=True)
        
        # Recursos completados según actividad del usuario
        recursos_completados = UserActivity.objects.filter(
            user=alumno, 
            actividad__icontains="visto material"
        ).count()
        
        # Tiempo de estudio total
        total_minutos = LearningSession.objects.filter(user=alumno).aggregate(
            total=models.Sum('duracion_minutos')
        )['total'] or 0
        tiempo_estudio = round(total_minutos / 60)  # en horas
        
        # Logros obtenidos según evaluaciones completadas
        logros_obtenidos = UserActivity.objects.filter(
            user=alumno,
            actividad__icontains="evaluacion completada"
        ).count()
        
        # Recursos nuevos: materiales que no ha visto
        vistos_ids = UserActivity.objects.filter(
            user=alumno,
            actividad__icontains="visto material"
        ).values_list('detalles', flat=True)
        
        # Filtrar IDs válidos
        recursos_vistos_ids = []
        for vid in vistos_ids:
            if vid and vid.isdigit():
                recursos_vistos_ids.append(int(vid))
        
        recursos_nuevos = recursos.exclude(id__in=recursos_vistos_ids).count()
        
    except Exception as e:
        # En caso de error, usar valores por defecto
        print(f"Error calculando estadísticas: {e}")
        user_cursos_count = 0
        recursos_completados = 0
        tiempo_estudio = 0
        logros_obtenidos = 0
        recursos_nuevos = 0
    
    context = {
        'user_cursos_count': user_cursos_count,
        'recursos_completados': recursos_completados,
        'tiempo_estudio': tiempo_estudio,
        'logros_obtenidos': logros_obtenidos,
        'recursos_nuevos': recursos_nuevos,
    }
    return render(request, 'dashboard_user.html', context)

@login_required
def progreso_estudiante(request):
    """Vista que muestra el progreso completo del estudiante en sus cursos"""
    alumno = request.user

    # ================================
    # 1. Cursos inscritos
    # ================================
    cursos_inscritos = (
        Inscripcion.objects
        .filter(alumno=alumno)
        .select_related('curso')
    )

    user_cursos_count = cursos_inscritos.count()

    # ================================
    # 2. Recursos completados (videos, lecturas, materiales)
    # ================================
    recursos_completados = UserActivity.objects.filter(
        user=alumno,
        actividad__icontains="visto material"
    ).count()

    # ================================
    # 3. Tiempo total de estudio (en horas)
    # ================================
    total_minutos = LearningSession.objects.filter(
        user=alumno
    ).aggregate(
        total=models.Sum('duracion_minutos')
    )['total'] or 0

    tiempo_estudio = round(total_minutos / 60)

    # ================================
    # 4. Logros (evaluaciones completadas)
    # ================================
    logros_obtenidos = UserActivity.objects.filter(
        user=alumno,
        actividad__icontains="evaluacion completada"
    ).count()

    # ================================
    # 5. ACTIVIDADES / TAREAS / EXÁMENES POR CURSO
    # ================================
    progreso_detallado = []

    for inscripcion in cursos_inscritos:
        curso = inscripcion.curso

        # Total de actividades del curso
        total_actividades = Actividad.objects.filter(curso=curso).count()

        # Actividades completadas por el usuario
        actividades_completadas = UserActivity.objects.filter(
            user=alumno,
            actividad__icontains="actividad completada",
            curso=curso
        ).count()

        # Total de evaluaciones
        total_evaluaciones = Evaluacion.objects.filter(curso=curso).count()

        # Evaluaciones completadas
        evaluaciones_completadas = UserActivity.objects.filter(
            user=alumno,
            actividad__icontains="evaluacion completada",
            curso=curso
        ).count()

        # Total de tareas
        total_tareas = Tarea.objects.filter(curso=curso).count()

        # Tareas entregadas
        tareas_entregadas = UserActivity.objects.filter(
            user=alumno,
            actividad__icontains="tarea entregada",
            curso=curso
        ).count()

        # Cálculo de progreso general
        total_items = total_actividades + total_evaluaciones + total_tareas
        completados = actividades_completadas + evaluaciones_completadas + tareas_entregadas

        progreso_porcentaje = round((completados / total_items) * 100) if total_items > 0 else 0

        progreso_detallado.append({
            "curso": curso,
            "inscripcion": inscripcion,
            "progreso": progreso_porcentaje,
            "total_actividades": total_actividades,
            "actividades_completadas": actividades_completadas,
            "total_evaluaciones": total_evaluaciones,
            "evaluaciones_completadas": evaluaciones_completadas,
            "total_tareas": total_tareas,
            "tareas_entregadas": tareas_entregadas,
        })

    # ================================
    # CONTEXTO FINAL
    # ================================
    context = {
        'user_cursos_count': user_cursos_count,
        'recursos_completados': recursos_completados,
        'tiempo_estudio': tiempo_estudio,
        'logros_obtenidos': logros_obtenidos,
        'cursos_inscritos': cursos_inscritos,
        'progreso_detallado': progreso_detallado,
    }

    return render(request, 'progreso_estudiante.html', context)



# ---------------------------
# GESTIÓN DE CURSOS
# ---------------------------

@login_required
def crear_curso(request):
    """Vista para que el profesor cree un nuevo curso."""
    if not request.user.is_staff:
        messages.error(request, "No tienes permiso para crear cursos.")
        return redirect("dashboard_user")
    
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        categoria = request.POST.get("categoria")
        
        if not nombre or not descripcion:
            messages.error(request, "Por favor completa todos los campos.")
            return redirect("crear_curso")
        
        # Crear curso asociado al profesor
        Curso.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            categoria=categoria,
            profesor=request.user
        )
        messages.success(request, "📘 Curso creado correctamente.")
        return redirect("dashboard_profesor")
    
    return render(request, "crear_curso.html")

@login_required
def cursos_disponibles(request):
    cursos = Curso.objects.exclude(inscritos__alumno=request.user)
    return render(request, "cursos_disponibles.html", {"cursos": cursos})

@login_required
def inscribirse_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    Inscripcion.objects.get_or_create(alumno=request.user, curso=curso)
    messages.success(request, f"✅ Te has inscrito en {curso.nombre}.")
    return redirect("cursos_disponibles")

@login_required
def mis_recursos(request):
    alumno = request.user

    # Obtener cursos donde el alumno está inscrito
    cursos_ids = Inscripcion.objects.filter(
    alumno=alumno
    ).values_list("curso_id", flat=True)


    # Obtener materiales visibles de esos cursos
    materiales = MaterialDidactico.objects.filter(
    curso_id__in=cursos_ids
    ).order_by("-fecha_subida")

    context = {
        "materiales": materiales
    }

    return render(request, "mis_recursos.html", context)



@login_required
def detalle_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)

    # Actividades y tareas del curso
    actividades = Actividad.objects.filter(curso=curso)
    tareas = Tarea.objects.filter(curso=curso)
    
    # Entregas del usuario (solo para marcar si la tarea ya fue entregada)
    entregas_qs = EntregaTarea.objects.filter(alumno=request.user, tarea__curso=curso)
    entregas_dict = {entrega.tarea.id: entrega for entrega in entregas_qs}

    # Solo si es profesor
    if hasattr(request.user, "perfilusuario") and getattr(request.user.perfilusuario, "is_teacher", False):
        materiales = MaterialDidactico.objects.filter(curso=curso)
        alumnos = Inscripcion.objects.filter(curso=curso).select_related('alumno')
        url_volver = reverse('dashboard:profesor_cursos')
    else:
        materiales = []
        alumnos = []
        url_volver = reverse('dashboard:dashboard_user')

    context = {
        "curso": curso,
        "actividades": actividades,
        "tareas": tareas,
        "entregas_dict": entregas_dict,  # 🔹 Esto es clave para mostrar entregas
        "materiales": materiales,
        "alumnos": alumnos,
        "url_volver": url_volver
    }

    return render(request, "detalle_curso.html", context)



@login_required
def editar_curso(request, curso_id):
    """Permite al profesor editar la información de un curso existente."""
    curso = get_object_or_404(Curso, id=curso_id, profesor=request.user)
    
    if request.method == "POST":
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ El curso se actualizó correctamente.")
            return redirect("dashboard:profesor_cursos")
    else:
        form = CursoForm(instance=curso)
    
    context = {
        "form": form,
        "curso": curso
    }
    return render(request, "editar_curso.html", context)

@login_required
def asignar_material_a_curso(request, material_id):
    try:
        material = MaterialDidactico.objects.get(id=material_id, profesor=request.user)
    except MaterialDidactico.DoesNotExist:
        messages.error(request, "❌ No se encontró el material.")
        return redirect('profesor_material')
    
    if request.method == 'POST':
        curso_id = request.POST.get('curso')
        try:
            curso = Curso.objects.get(id=curso_id, profesor=request.user)
            material.curso = curso
            material.save()
            messages.success(request, f"✅ Material asignado correctamente al curso {curso.nombre}.")
        except Curso.DoesNotExist:
            messages.error(request, "⚠️ Curso no válido.")
    
    return redirect('profesor_material')

# ---------------------------
# GESTIÓN DE EVALUACIONES
# ---------------------------

@login_required
def crear_evaluacion(request):
    # 🔹 Obtener solo los cursos del profesor actual
    cursos = Curso.objects.filter(profesor=request.user)
    
    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        if form.is_valid():
            evaluacion = form.save(commit=False)
            evaluacion.profesor = request.user
            evaluacion.save()
            messages.success(request, "✅ Evaluación creada correctamente.")
            return redirect('dashboard:profesor_evaluaciones')
    else:
        form = EvaluacionForm()
    
    # 🔹 Limitar el campo 'curso' a los cursos del profesor logueado
    form.fields['curso'].queryset = cursos
    
    return render(request, 'crear_evaluacion.html', {'form': form, 'cursos': cursos})

@login_required
def editar_evaluacion(request, evaluacion_id):
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id, profesor=request.user)
    cursos = Curso.objects.filter(profesor=request.user)
    
    if request.method == 'POST':
        form = EvaluacionForm(request.POST, instance=evaluacion)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Evaluación actualizada correctamente.")
            return redirect('dashboard:profesor_evaluaciones')
    else:
        form = EvaluacionForm(instance=evaluacion)
        form.fields['curso'].queryset = cursos
    
    return render(request, 'editar_evaluacion.html', {'form': form, 'evaluacion': evaluacion})

@login_required
def eliminar_evaluacion(request, evaluacion_id):
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id, profesor=request.user)
    evaluacion.delete()
    messages.success(request, "🗑️ Evaluación eliminada correctamente.")
    return redirect('dashboard:profesor_evaluaciones')

@login_required
def detalle_evaluacion(request, evaluacion_id):
    """Muestra el detalle de una evaluación y permite agregar materiales del curso"""
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id, profesor=request.user)
    curso = evaluacion.curso
    
    # 🔹 Materiales ya asociados a esta evaluación
    materiales_asignados = evaluacion.materiales.all()
    
    # 🔹 Materiales disponibles para agregar (del curso del profesor)
    materiales_disponibles = MaterialDidactico.objects.filter(curso=curso, profesor=request.user)
    
    # 🔹 Agregar material seleccionado a la evaluación
    if request.method == "POST":
        material_id = request.POST.get("material_id")
        if material_id:
            try:
                material = MaterialDidactico.objects.get(id=material_id, curso=curso, profesor=request.user)
                evaluacion.materiales.add(material)
                messages.success(request, f"📘 El material '{material.titulo}' se agregó a la evaluación correctamente.")
            except MaterialDidactico.DoesNotExist:
                messages.error(request, "❌ El material seleccionado no existe o no pertenece a este curso.")
            return redirect("dashboard:detalle_evaluacion", evaluacion_id=evaluacion.id)
    
    context = {
        "evaluacion": evaluacion,
        "curso": curso,
        "materiales_asignados": materiales_asignados,
        "materiales_disponibles": materiales_disponibles,
    }
    return render(request, "detalle_evaluacion.html", context)

@login_required
def quitar_material_evaluacion(request, evaluacion_id, material_id):
    """Elimina la relación entre un material y una evaluación (sin borrar el archivo)."""
    evaluacion = get_object_or_404(Evaluacion, id=evaluacion_id, profesor=request.user)
    try:
        material = evaluacion.materiales.get(id=material_id)
        evaluacion.materiales.remove(material)
        messages.success(request, f"🗑️ El material '{material.titulo}' se quitó de la evaluación.")
    except MaterialDidactico.DoesNotExist:
        messages.error(request, "❌ El material no pertenece a esta evaluación.")
    
    return redirect("detalle_evaluacion", evaluacion_id=evaluacion.id)

# ---------------------------
# APIs y VISTAS DE IA
# ---------------------------

def ai_stats_api(request):
    total_users = User.objects.count()
    total_students = User.objects.filter(groups__name='Alumno').count()
    total_teachers = User.objects.filter(groups__name='Profesor').count()
    total_admins = User.objects.filter(is_staff=True).count()
    
    data = {
        'total_users': total_users,
        'students': total_students,
        'teachers': total_teachers,
        'admins': total_admins
    }
    return JsonResponse(data)

@staff_member_required
def admin_distribution_view(request):
    total_users = User.objects.count()
    students = User.objects.filter(groups__name='Alumno').count()
    teachers = User.objects.filter(groups__name='Profesor').count()
    admins = User.objects.filter(is_staff=True).count()
    
    context = {
        'total_users': total_users,
        'students': students,
        'teachers': teachers,
        'admins': admins
    }
    return render(request, 'admin_dashboard.html', context)

@csrf_exempt
def ai_chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '').lower()
        
        # Aquí puedes mejorar la lógica con IA real más adelante
        if "hola" in user_message:
            reply = "¡Hola! Soy tu asistente de EduConnect 🤖. ¿En qué puedo ayudarte hoy?"
        elif "ayuda" in user_message:
            reply = "Puedo ayudarte a entender tus tareas, revisar tus clases o mostrar estadísticas."
        else:
            reply = "No entendí bien eso 😅, ¿puedes reformularlo?"
        
        return JsonResponse({'reply': reply})

@csrf_exempt
def ai_recommendations_api(request):
    """API sencilla de recomendaciones IA."""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)
    
    role = "Alumno"
    if request.user.groups.filter(name="Profesor").exists():
        role = "Profesor"
    elif request.user.is_staff:
        role = "Administrador"
    
    # Ejemplo de recomendaciones simples
    if role == "Profesor":
        recommendations = [
            "📚 Sube tus materiales didácticos actualizados.",
            "🧠 Usa el chat IA para generar preguntas tipo examen.",
            "📊 Revisa la participación de tus alumnos en clase."
        ]
    elif role == "Alumno":
        recommendations = [
            "🕒 No olvides revisar tus tareas pendientes.",
            "🤖 Usa el chat IA para estudiar temas difíciles.",
            "💡 Participa en los foros para subir tu calificación."
        ]
    else:
        recommendations = [
            "🧭 Administra usuarios desde el panel de control.",
            "📈 Consulta la distribución de usuarios.",
            "🧩 Supervisa las interacciones de IA."
        ]
    
    return JsonResponse({
        'role': role,
        'recommendations': recommendations
    })

@user_passes_test(lambda u: u.is_staff)
def admin_user_distribution(request):
    """Vista para mostrar la distribución de usuarios"""
    total_users = User.objects.count()
    total_staff = User.objects.filter(is_staff=True).count()
    total_professors = User.objects.filter(groups__name='Profesor').count()
    total_students = total_users - total_staff - total_professors
    
    # Datos para Plotly
    data = {
        "labels": ["Administradores", "Profesores", "Alumnos"],
        "values": [total_staff, total_professors, total_students]
    }
    
    context = {
        "data": data,
        "total_users": total_users
    }
    return render(request, "user_distribution.html", context)

@user_passes_test(lambda u: u.is_superuser)
def admin_distribution_plotly_view(request):
    """Vista con gráfica Plotly para distribución de usuarios"""
    users = User.objects.all()
    data = {
        'Tipo': ['Superusuario' if u.is_superuser else 'Staff' if u.is_staff else 'Usuario' for u in users]
    }
    
    df = pd.DataFrame(data)
    fig = px.pie(
        df, 
        names='Tipo',
        title='Distribución de Usuarios en EduConnect',
        color_discrete_sequence=px.colors.qualitative.Set3,
        hole=0.3
    )
    fig.update_traces(textinfo='percent+label')
    chart_html = fig.to_html(full_html=False)
    
    return render(request, 'admin_dashboard/distribution.html', {
        'chart_html': chart_html
    })

from django.shortcuts import render, get_object_or_404
from .models import Curso, Actividad, Tarea, EntregaTarea


