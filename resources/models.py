# resources/models.py
from django.db import models
from django.contrib.auth.models import User

class Recursos(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to="recursos/", null=True, blank=True)  
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_completado = models.DateField(null=True, blank=True)
    completado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Curso

class EntregaAlumno(models.Model):
    alumno = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey('dashboard.Curso', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='entregas/')
    tipo = models.CharField(max_length=50, blank=True, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.alumno.username}"
