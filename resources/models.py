# resources/models.py
from django.db import models
from django.contrib.auth.models import User

class Recursos(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to="recursos/", null=True, blank=True)  # 👈 para subir archivos
    fecha_completado = models.DateField(null=True, blank=True)
    completado = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo
