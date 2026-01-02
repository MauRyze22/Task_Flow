from django import forms
from .models import Equipo, Proyecto, Tarea, Comentario, Perfil
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = '__all__'
        

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        

class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = '__all__'
        
        
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = '__all__'
        exclude = ['user']
        
        
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    numero = forms.CharField(max_length = 20, required = False)
    
         
         
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
        exclude = ['user']