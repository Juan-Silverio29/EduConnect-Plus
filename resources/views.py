from django.shortcuts import render, redirect, get_object_or_404
from .models import Recursos
from .forms import RecursoForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# 📌 Lista de recursos (solo los del usuario, admin ve todos)
@login_required
def lista_recursos(request):
    if request.user.is_superuser:
        recursos = Recursos.objects.all().order_by("-id")
    else:
        recursos = Recursos.objects.filter(autor=request.user).order_by("-id")
    return render(request, "lista_recursos.html", {"recursos": recursos})


# 📍 Subir recurso nuevo
@login_required
def subir_recurso(request):
    if request.method == "POST":
        form = RecursoForm(request.POST, request.FILES)
        if form.is_valid():
            recurso = form.save(commit=False)
            recurso.autor = request.user  # 👈 Guardar quién subió el recurso
            recurso.save()
            messages.success(request, "✅ Recurso subido correctamente.")
            return redirect("lista_recursos")
    else:
        form = RecursoForm()
    return render(request, "subir_recurso.html", {"form": form})


# 📍 Editar recurso (solo el autor o admin)
@login_required
def editar_recurso(request, recurso_id):
    recurso = get_object_or_404(Recursos, id=recurso_id)

    if recurso.autor != request.user and not request.user.is_superuser:
        messages.warning(request, "⚠️ No tienes permiso para editar este recurso.")
        return redirect("lista_recursos")

    if request.method == "POST":
        form = RecursoForm(request.POST, request.FILES, instance=recurso)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Recurso actualizado correctamente.")
            return redirect("lista_recursos")
    else:
        form = RecursoForm(instance=recurso)
    return render(request, "editar_recurso.html", {"form": form, "recurso": recurso})


# 📍 Eliminar recurso (solo el autor o admin)
@login_required
def eliminar_recurso(request, recurso_id):
    recurso = get_object_or_404(Recursos, id=recurso_id)

    if recurso.autor != request.user and not request.user.is_superuser:
        messages.warning(request, "⚠️ No puedes eliminar un recurso que no es tuyo.")
        return redirect("lista_recursos")

    if request.method == "POST":
        recurso.delete()
        messages.success(request, "🗑️ Recurso eliminado correctamente.")
        return redirect("lista_recursos")
    return render(request, "eliminar_recurso.html", {"recurso": recurso})


# 📈 Logros y recursos completados
def logros_recursos_completados(request):
    recursos = Recursos.objects.filter(completado=True)
    total_recursos = Recursos.objects.count()

    progreso = int((recursos.count() / total_recursos) * 100) if total_recursos > 0 else 0

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
