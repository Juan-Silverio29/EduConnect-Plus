# resources/models.py
from django.db import models
from django.contrib.auth.models import User

class Recursos(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=100)
    url = models.URLField(blank=True, null=True)
    descargable = models.BooleanField(default=False)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)  # 👈 agregamos campo para logros
    fecha_completado = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.titulo
