from django import forms
from django.contrib.auth.forms import UserCreationForm
# Importamos tus modelos locales correctos
from .models import Usuario, Recetas 

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_seller = forms.BooleanField(required=False)

    class Meta:
        model = Usuario  # <-- Cambiado a tu modelo personalizado 'Usuario'
        fields = ('username', 'email', 'is_seller')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Recetas  # <-- Cambiado al nombre real de tu modelo 'Recetas'
        # Usamos los campos reales que existen en tu clase Recetas:
        fields = ['name', 'description', 'dificultad', 'ingredientes', 'categories']
        widgets = {
            'categories': forms.CheckboxSelectMultiple()
        }