from django import forms
from django.forms.fields import ChoiceField
from django.forms.widgets import CheckboxInput, NumberInput, Select, TextInput

from .models import Mascota,Nota


class MascotaRegisterForm(forms.ModelForm):

    TIPO_CHOICES=(
        ('Gato','Gato'),
        ('Perro','Perro'),
    )

    ACTIVIDAD_CHOICES=(
        ('Poca','Poca'),
        ('Normal','Normal'),
        ('Moderada','Moderada'),
        ('Intensa','Intensa'),
    )

    TAMAÑO_CHOICES=(
        ('Muy pequeño','Muy pequeño'),
        ('Pequeño','Pequeño'),
        ('Mediano','Mediano'),
        ('Grande','Grande'),
        ('Gigante','Gigante'),
    )

    OBJETIVO_CHOICES=(
        ('Bajar peso','Bajar peso'),
        ('Mantener peso','Mantener peso'),
        ('Aumentar peso','Aumentar peso'),
    )

    nombre=forms.CharField(
         
        label='Nombre',
        max_length=30,
        required=True,
        help_text='Ingrese nombre de la mascota',
        widget=forms.TextInput(
        
        attrs={
            'placeholder':'Perrinho',
            'title':'Ingrese el nombre de su mascota',
        }
    ))

    tipo=forms.ChoiceField(
        choices=TIPO_CHOICES, 
        label='Tipo de mascota',
        required=True,
        widget=forms.Select(

        attrs={
            
        }
    ))

    edad=forms.CharField(
         
        label='Edad',
        required=True,
        help_text='Ingrese la edad de su mascota',
        widget=forms.NumberInput(

        attrs={
            'placeholder':'25',
            'min':'0',
            'max':'300',
            'step':'1',
            'title':'Ingrese la edad de la mascota'
        }
    ))

    peso=forms.CharField(
         
        label='Peso',
        required=True,
        help_text='Ingrese el peso de su mascota',
        widget=forms.NumberInput(

        attrs={
            'placeholder':'25',
            'min':'0',
            'max':'400',
            'step':'0.1',
            'title':'Ingrese el peso en kg de su mascota',
        }
    ))

    actividad=forms.ChoiceField(
        choices=ACTIVIDAD_CHOICES, 
        label='Actividad',
        required=True,
        widget=forms.Select(

        attrs={
            
        }
    ))

    tamaño=forms.ChoiceField(
        choices=TAMAÑO_CHOICES, 
        label='Tamaño',
        required=True,
        widget=forms.Select(

        attrs={
            
        }
    ))

    objetivo=forms.ChoiceField(
        choices=OBJETIVO_CHOICES, 
        label='Objetivo',
        required=True,
        widget=forms.Select(

        attrs={
            
        }
    ))

    esterilizado=forms.BooleanField(
        label='Esterilizado',
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                'title':'Tildado = si'
            }
        )
    )

    imagen=forms.FileField(
        required=True,
        label="Imagen de la mascota",
    )

    class Meta:
        model=Mascota
        fields=(
            'nombre',
            'tipo',
            'edad',
            'peso',
            'actividad',
            'tamaño',
            'objetivo',
            'esterilizado',
            'imagen'
        )
 

    
    def clean(self):
        cleaned_data=super(MascotaRegisterForm, self).clean() 
        peso = self.cleaned_data.get('peso')    
        edad = self.cleaned_data.get('edad')

            
        if peso<=0:
            self.add_error('peso','Por favor ponga un peso distinto o mayor a 0')
        if edad<=0:
            self.add_error('edad','Por favor ingrese una edad mayor o igual a 0 meses')  

                    
        return cleaned_data

class MascotaUpdateForm(forms.ModelForm):

    class Meta:
        model=Mascota
        fields=(
            'nombre',
            'tipo',
            'edad',
            'peso',
            'actividad',
            'tamaño',
            'esterilizado',
            'objetivo',
            'imagen',
        )

    def __init__(self, *args, **kwargs):
        #saco el id de los kwargs
        self.mascotaid=kwargs.pop('pk','')
        #llamamos al constructor de la clase padre
        super(MascotaUpdateForm, self).__init__(*args, **kwargs)

        #y podemos acceder a las propiedades de los campos
        mascota=Mascota.objects.get(pk=self.mascotaid)

        self.fields['nombre'].initial=mascota.nombre
        self.fields['tipo'].initial=mascota.tipo
        self.fields['edad'].initial=mascota.edad
        self.fields['peso'].initial=mascota.peso
        self.fields['actividad'].initial=mascota.actividad
        self.fields['tamaño'].initial=mascota.tamaño
        self.fields['esterilizado'].initial=mascota.esterilizado
        self.fields['objetivo'].initial=mascota.objetivo


    def clean(self):
        
        cleaned_data=super(MascotaUpdateForm, self).clean()

        peso = self.cleaned_data.get('peso')    
        edad = self.cleaned_data.get('edad')

            
        if peso<=0:
            self.add_error('peso','Por favor ponga un peso distinto o mayor a 0')
        if edad<=0:
            self.add_error('edad','Por favor ingrese una edad mayor o igual a 0 meses')  

                    
            
        return cleaned_data
    
class AgregarNotaForm(forms.ModelForm):

    fecha=forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    

    class Meta:
        model=Nota
        fields=(
            'importancia',
            'texto',
        )



