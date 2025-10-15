from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Foro, Comentario
from .forms import ForoForm, ComentarioForm

# 📄 Listar todos los foros
@login_required
def foro_lista(request):
    foros = Foro.objects.all().order_by("-fecha_creacion")
    return render(request, "foros.html", {"foros": foros})


# ✏️ Crear nuevo foro
@login_required
def crear_foro(request):
    if request.method == "POST":
        form = ForoForm(request.POST, request.FILES)  # aceptar archivos adjuntos
        if form.is_valid():
            foro = form.save(commit=False)
            foro.autor = request.user  # guarda quién lo creó
            foro.save()
            messages.success(request, "✅ Foro creado correctamente.")
            return redirect("foros")
    else:
        form = ForoForm()
    return render(request, "crear_foro.html", {"form": form})


# 👁️ Ver detalle del foro y agregar comentarios
@login_required
def foro_detalle(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id)
    comentarios = foro.comentarios.all().order_by("-fecha")

    if request.method == "POST":
        form = ComentarioForm(request.POST, request.FILES)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.foro = foro
            comentario.autor = request.user
            comentario.save()
            messages.success(request, "💬 Comentario agregado correctamente.")
            return redirect("foro_detalle", foro_id=foro.id)
    else:
        form = ComentarioForm()

    return render(
        request,
        "foro_detalle.html",
        {"foro": foro, "comentarios": comentarios, "form": form}
    )


# ✏️ Editar foro (solo el autor)
@login_required
def editar_foro(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id)

    if foro.autor != request.user:
        messages.warning(request, "⚠️ No tienes permiso para editar este foro.")
        return redirect("foros")

    if request.method == "POST":
        form = ForoForm(request.POST, request.FILES, instance=foro)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Foro actualizado correctamente.")
            return redirect("foros")
    else:
        form = ForoForm(instance=foro)
    return render(request, "editar_foro.html", {"form": form, "foro": foro})


# 🗑️ Eliminar foro (solo el autor)
@login_required
def eliminar_foro(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id)

    if foro.autor != request.user:
        messages.warning(request, "⚠️ No tienes permiso para eliminar este foro.")
        return redirect("foros")

    if request.method == "POST":
        foro.delete()
        messages.success(request, "🗑️ Foro eliminado correctamente.")
        return redirect("foros")

    return render(request, "eliminar_foro.html", {"foro": foro})


# ✏️ Editar comentario (solo el autor)
@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    if comentario.autor != request.user:
        messages.warning(request, "⚠️ No tienes permiso para editar este comentario.")
        return redirect("foro_detalle", foro_id=comentario.foro.id)

    if request.method == "POST":
        form = ComentarioForm(request.POST, request.FILES, instance=comentario)
        if form.is_valid():
            form.save()
            messages.success(request, "💬 Comentario actualizado correctamente.")
            return redirect("foro_detalle", foro_id=comentario.foro.id)
    else:
        form = ComentarioForm(instance=comentario)
    return render(request, "editar_comentario.html", {"form": form, "comentario": comentario})


# 🗑️ Eliminar comentario (solo el autor)
@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    if comentario.autor != request.user:
        messages.warning(request, "⚠️ No tienes permiso para eliminar este comentario.")
        return redirect("foro_detalle", foro_id=comentario.foro.id)

    if request.method == "POST":
        foro_id = comentario.foro.id
        comentario.delete()
        messages.success(request, "🗑️ Comentario eliminado correctamente.")
        return redirect("foro_detalle", foro_id=foro_id)

    return render(request, "eliminar_comentario.html", {"comentario": comentario})
