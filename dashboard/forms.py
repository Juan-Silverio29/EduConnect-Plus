# dashboard/forms.py
from django import forms
from .models import MaterialDidactico
from auth_app.models import PerfilUsuario

class MaterialForm(forms.ModelForm):
    class Meta:
        model = MaterialDidactico
        fields = ['titulo', 'tipo', 'archivo', 'enlace']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Guía de estudio Unidad 1'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'archivo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'enlace': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }

class EditarPerfilForm(forms.ModelForm):
    username = forms.CharField(label="Usuario", max_length=150, required=False, disabled=True)
    first_name = forms.CharField(label="Nombre", max_length=150, required=False)
    last_name = forms.CharField(label="Apellido", max_length=150, required=False)
    institucion = forms.CharField(label="Institución", max_length=150, required=False)

    class Meta:
        model = PerfilUsuario
        fields = ['foto_perfil', 'institucion']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.user.username
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name
        self.fields['institucion'].initial = self.instance.institucion

    def save(self, commit=True):
        perfil = super().save(commit=False)
        self.user.first_name = self.cleaned_data.get('first_name')
        self.user.last_name = self.cleaned_data.get('last_name')
        perfil.institucion = self.cleaned_data.get('institucion')
        if commit:
            self.user.save()
            perfil.save()
        return perfil
