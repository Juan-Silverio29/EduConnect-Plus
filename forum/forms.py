from django import forms
from .models import Foro, Comentario

class ForoForm(forms.ModelForm):
    class Meta:
        model = Foro
        fields = ["titulo", "descripcion"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control", "placeholder": "Escribe el título del tema"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "placeholder": "Escribe la descripción"}),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["texto"]
        widgets = {
            "texto": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Escribe tu comentario"}),
        }
