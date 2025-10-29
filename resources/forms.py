from django import forms
from .models import Recursos
from django import forms
from .models import EntregaAlumno

class RecursoForm(forms.ModelForm):
    class Meta:
        model = Recursos
        fields = ['titulo', 'descripcion', 'archivo', 'completado', 'fecha_completado']

class EntregaAlumnoForm(forms.ModelForm):
    class Meta:
        model = EntregaAlumno
        fields = ['curso', 'titulo', 'archivo']
        widgets = {
            'curso': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del archivo'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }