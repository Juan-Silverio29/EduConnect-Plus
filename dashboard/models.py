# dashboard/models.py
from django.db import models
from django.contrib.auth.models import User

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard_perfil')
    institucion = models.CharField(max_length=255)
    foto_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class MaterialDidactico(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    tipo = models.CharField(max_length=50, blank=True, null=True)
    enlace = models.URLField(blank=True, null=True)
    archivo = models.FileField(upload_to='materiales/', blank=True, null=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Curso(models.Model):
    nombre = models.CharField(max_length=255)
    grupo = models.CharField(max_length=50)
    profesor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='cursos')
    alumnos = models.ManyToManyField(User, blank=True, related_name='cursos_inscritos')
    descripcion = models.TextField(blank=True, null=True)
