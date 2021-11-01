from django import forms
from django.forms.fields import ChoiceField
from django.forms.widgets import CheckboxInput, NumberInput, Select, TextInput

from .models import Mascota,Nota


class MascotaRegisterForm(forms.ModelForm):

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
            'imagen'
        )

        
        widgets={
            'nombre':TextInput(attrs={'title':"Ingrese el nombre de la mascota"}),
            'tipo':Select(attrs={'title':'Seleccione el tipo de mascota'}),
            'edad':NumberInput(attrs={'title':'Edad en meses'}),
            'peso':NumberInput(attrs={'title':'Peso en kg'}),
            'actividad':Select(attrs={'title':'Seleccione cuanta actividad realiza'}),
            'tamaño':Select(attrs={'title':'Seleccione el tamaño de la mascota'}),
            'objetivo':Select(attrs={'title':'Seleccione el objetivo que desea alcanzar'}),
            'esterilizado':CheckboxInput(attrs={'title':'Tildado = si'})

        }

    def clean_peso(self):
            peso = self.cleaned_data.get('peso')
            
            if peso<=0:
                raise forms.ValidationError('Por favor ponga un peso distinto o mayor a 0')


            return peso

    def clean_edad(self):
            edad = self.cleaned_data.get('edad')
            
            if edad<=0:
                raise forms.ValidationError('Por favor ingrese una edad mayor a 0 meses')    


            return edad

    
    def clean(self):
        cleaned_data=super(MascotaRegisterForm, self).clean()     
                    
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


    def clean_peso(self):
            peso = self.cleaned_data.get('peso')
            
            if peso<=0:
                raise forms.ValidationError('Por favor ponga un peso distinto o mayor a 0')


            return peso

    def clean_edad(self):
            edad = self.cleaned_data.get('edad')
            
            if edad<=0:
                raise forms.ValidationError('Por favor ingrese una edad mayor a 0 meses')    


            return edad


    
    def clean(self):
        
        cleaned_data=super(MascotaUpdateForm, self).clean()
            
        return cleaned_data
    
class AgregarNotaForm(forms.ModelForm):

    fecha=forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    

    class Meta:
        model=Nota
        fields=(
            'importancia',
            'texto',
        )



