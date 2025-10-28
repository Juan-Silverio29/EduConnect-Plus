from django.db import models
from django.contrib.auth.models import User

# 🧑‍🏫 Modelo de Curso creado por un profesor
class Curso(models.Model):
    CATEGORIAS = [
        ("Ciencias", "Ciencias"),
        ("Matemáticas", "Matemáticas"),
        ("Programación", "Programación"),
        ("Idiomas", "Idiomas"),
        ("Física", "Física"),
        ("Música", "Música"),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default="Ciencias")
    profesor = models.ForeignKey(User, on_delete=models.CASCADE)
    grupo = models.CharField(max_length=50, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return self.nombre


# 👨‍🎓 Modelo de Inscripción (relación alumno-curso)
class Inscripcion(models.Model):
    alumno = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inscripciones")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="inscritos")
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('alumno', 'curso')

    def __str__(self):
        return f"{self.alumno.username} → {self.curso.nombre}"


# 📚 Actualiza tu modelo MaterialDidactico para vincularlo con cursos
class MaterialDidactico(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="materiales", null=True, blank=True)
    profesor = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    archivo = models.FileField(upload_to='materiales/', blank=True, null=True)
    enlace = models.URLField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

# 📘 Modelo de Evaluaciones
class Evaluacion(models.Model):
    profesor = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey('Curso', on_delete=models.CASCADE, related_name='evaluaciones')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    creada_en = models.DateTimeField(auto_now_add=True)
    
    # 👇 NUEVO CAMPO: relación directa con MaterialDidactico
    materiales = models.ManyToManyField('MaterialDidactico', blank=True, related_name='evaluaciones_asignadas')

    def __str__(self):
        return f"{self.nombre} - {self.curso.nombre}"
