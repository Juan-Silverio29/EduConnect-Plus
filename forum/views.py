from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Foro, Comentario
from .forms import ForoForm, ComentarioForm

# Listar todos los foros
@login_required
def foro_lista(request):
    foros = Foro.objects.all().order_by("-fecha_creacion")
    return render(request, "foros.html", {"foros": foros})


# Crear nuevo foro
@login_required
def crear_foro(request):
    if request.method == "POST":
        form = ForoForm(request.POST, request.FILES)  # 👈 aceptar archivos
        if form.is_valid():
            foro = form.save(commit=False)
            foro.autor = request.user
            foro.save()
            return redirect("foros")
    else:
        form = ForoForm()
    return render(request, "crear_foro.html", {"form": form})


# Ver detalle del foro y agregar comentarios
@login_required
def foro_detalle(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id)
    comentarios = foro.comentarios.all().order_by("-fecha")

    if request.method == "POST":
        form = ComentarioForm(request.POST, request.FILES)  # 👈 aceptar archivos
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.foro = foro
            comentario.autor = request.user
            comentario.save()
            return redirect("foro_detalle", foro_id=foro.id)
    else:
        form = ComentarioForm()

    return render(
        request,
        "foro_detalle.html",
        {"foro": foro, "comentarios": comentarios, "form": form}
    )


# Editar foro
@login_required
def editar_foro(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id, autor=request.user)
    if request.method == "POST":
        form = ForoForm(request.POST, request.FILES, instance=foro)
        if form.is_valid():
            form.save()
            return redirect("foros")
    else:
        form = ForoForm(instance=foro)
    return render(request, "editar_foro.html", {"form": form, "foro": foro})


# Eliminar foro
@login_required
def eliminar_foro(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id, autor=request.user)
    if request.method == "POST":
        foro.delete()
        return redirect("foros")
    return render(request, "eliminar_foro.html", {"foro": foro})


# Editar comentario
@login_required
def editar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id, autor=request.user)
    if request.method == "POST":
        form = ComentarioForm(request.POST, request.FILES, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect("foro_detalle", foro_id=comentario.foro.id)
    else:
        form = ComentarioForm(instance=comentario)
    return render(request, "editar_comentario.html", {"form": form, "comentario": comentario})


# Eliminar comentario
@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id, autor=request.user)
    if request.method == "POST":
        foro_id = comentario.foro.id
        comentario.delete()
        return redirect("foro_detalle", foro_id=foro_id)
    return render(request, "eliminar_comentario.html", {"comentario": comentario})
