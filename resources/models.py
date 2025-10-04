# resources/models.py
from django.db import models
from django.contrib.auth.models import User


class Recursos(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha_completado = models.DateField(null=True, blank=True)
    completado = models.BooleanField(default=False)  # 👈 nuevo campo


    def __str__(self):
        return self.titulo
