from django import forms
from .models import Recursos

class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recursos
        fields = ['titulo', 'descripcion', 'archivo', 'completado', 'fecha_completado']
