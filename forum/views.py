from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Foro, Comentario

#  Listar todos los foros
@login_required
def foro_lista(request):
    foros = Foro.objects.all().order_by("-fecha_creacion")
    return render(request, "foros.html", {"foros": foros})

# Crear nuevo foro
@login_required
def crear_foro(request):
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        descripcion = request.POST.get("descripcion")

        if titulo and descripcion:
            Foro.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                autor=request.user  
            )
            return redirect("foros")  # vuelve a la lista
    return render(request, "crear_foro.html")

# Ver detalle del foro y agregar comentarios
@login_required
def foro_detalle(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id)
    comentarios = foro.comentarios.all().order_by("-fecha")

    if request.method == "POST":
        texto = request.POST.get("texto")  
        if texto:
            Comentario.objects.create(
                foro=foro,
                autor=request.user,
                texto=texto
            )
            return redirect("foro_detalle", foro_id=foro.id)

    return render(request, "foro_detalle.html", {"foro": foro, "comentarios": comentarios})

#  Editar foro
@login_required
def editar_foro(request, foro_id):
    foro = get_object_or_404(Foro, id=foro_id, autor=request.user)
    if request.method == "POST":
        foro.titulo = request.POST.get("titulo")
        foro.descripcion = request.POST.get("descripcion")
        foro.save()
        return redirect("foros")
    return render(request, "editar_foro.html", {"foro": foro})

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
        comentario.texto = request.POST.get("texto")
        comentario.save()
        return redirect("foro_detalle", foro_id=comentario.foro.id)
    return render(request, "editar_comentario.html", {"comentario": comentario})

#  Eliminar comentario
@login_required
def eliminar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id, autor=request.user)
    if request.method == "POST":
        foro_id = comentario.foro.id
        comentario.delete()
        return redirect("foro_detalle", foro_id=foro_id)
    return render(request, "eliminar_comentario.html", {"comentario": comentario})
