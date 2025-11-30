from django import forms
from django.contrib.auth.models import User
from .models import *

class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellido = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    usuario = forms.CharField(max_length=150, required=False)
    telefono = forms.CharField(max_length=20, required=False)
    direccion = forms.CharField(max_length=200, required=False)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con ese email')
        return email

    def clean(self):
        cleaned = super().clean()
        pwd = cleaned.get('password')
        cpwd = cleaned.get('confirm_password')
        usuario = cleaned.get('usuario')
        if pwd and cpwd and pwd != cpwd:
            self.add_error('confirm_password', 'Las contraseñas no coinciden')
        if usuario and User.objects.filter(username=usuario).exists():
            self.add_error('usuario', 'Ya existe un usuario con ese nombre')
        return cleaned

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'fecha_nacimiento']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Max'}),
            'especie': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Perro, Gato'}),
            'raza': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Labrador'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha', 'hora', 'estado', 'mascota', 'veterinario']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'mascota': forms.Select(attrs={'class': 'form-select'}),
            'veterinario': forms.Select(attrs={'class': 'form-select'}),
        }

class VeterinarioForm(forms.ModelForm):
    class Meta:
        model = Veterinario
        fields = ['usuario', 'especialidad']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ej: Cirugía, Clínica General'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            rol_vet = Rol.objects.get(nombre_rol='Veterinario clínico')
            rol_vet_esp = Rol.objects.filter(nombre_rol='Veterinario especialista').first()
            qs = Usuario.objects.filter(models.Q(rol=rol_vet) | models.Q(rol=rol_vet_esp))
            self.fields['usuario'].queryset = qs
        except Rol.DoesNotExist:
            self.fields['usuario'].queryset = Usuario.objects.all()
