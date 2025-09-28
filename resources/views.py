from django.shortcuts import render
from .models import Recursos

def logros_recursos_completados(request):
    logros = [
        {"titulo": "Curso de Python Básico", "descripcion": "Completado el 10 de septiembre 2025"},
        {"titulo": "Introducción a SQL", "descripcion": "Completado el 15 de septiembre 2025"},
        {"titulo": "React para principiantes", "descripcion": "Completado el 20 de septiembre 2025"},
    ]
    return render(request, "logros_recursos_completados.html", {"logros": logros})

def logros_recursos_completados(request):
    logros = Recursos.objects.filter(completado=True)
    return render(request, "logros_recursos_completados.html", {"logros": logros})