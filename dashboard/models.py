from django.db import models
from django.contrib.auth.models import User

class MaterialDidactico(models.Model):
    profesor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=150)
    tipo = models.CharField(
        max_length=50,
        choices=[
            ("PDF", "PDF"),
            ("Presentación", "Presentación"),
            ("Video", "Video"),
            ("Enlace", "Enlace"),
            ("Otro", "Otro"),
        ]
    )
    archivo = models.FileField(upload_to='materiales/', blank=True, null=True)
    enlace = models.URLField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.profesor.username})"
