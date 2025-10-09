from django.shortcuts import render, redirect, get_object_or_404
from .models import Recursos
from .forms import RecursoForm
from django.contrib.auth.decorators import login_required

# 📌 Lista de recursos
@login_required
def lista_recursos(request):
    recursos = Recursos.objects.all()
    return render(request, "lista_recursos.html", {"recursos": recursos})

# 📍 Subir recurso nuevo
@login_required
def subir_recurso(request):
    if request.method == "POST":
        form = RecursoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("lista_recursos")
    else:
        form = RecursoForm()
    return render(request, "subir_recurso.html", {"form": form})

# 📍 Editar recurso
@login_required
def editar_recurso(request, recurso_id):
    recurso = get_object_or_404(Recursos, id=recurso_id)
    if request.method == "POST":
        form = RecursoForm(request.POST, request.FILES, instance=recurso)
        if form.is_valid():
            form.save()
            return redirect("lista_recursos")
    else:
        form = RecursoForm(instance=recurso)
    return render(request, "editar_recurso.html", {"form": form, "recurso": recurso})

# 📍 Eliminar recurso
@login_required
def eliminar_recurso(request, recurso_id):
    recurso = get_object_or_404(Recursos, id=recurso_id)
    if request.method == "POST":
        recurso.delete()
        return redirect("lista_recursos")
    return render(request, "eliminar_recurso.html", {"recurso": recurso})


def logros_recursos_completados(request):
    recursos = Recursos.objects.filter(completado=True)
    total_recursos = Recursos.objects.count()

    # Calcular progreso en porcentaje
    if total_recursos > 0:
        progreso = int((recursos.count() / total_recursos) * 100)
    else:
        progreso = 0

    # Definir clase de color según progreso
    if progreso < 40:
        progreso_class = "bg-danger"
    elif progreso < 70:
        progreso_class = "bg-warning"
    else:
        progreso_class = "bg-success"

    return render(request, "logros_recursos_completados.html", {
        "recursos": recursos,
        "total_recursos": total_recursos,
        "progreso": progreso,
        "progreso_class": progreso_class
    })
