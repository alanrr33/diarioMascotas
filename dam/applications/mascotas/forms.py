from django import forms
from django.forms.widgets import NumberInput

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
    
    def clean(self):
        cleaned_data=super(MascotaRegisterForm, self).clean()

        #prevengo que ingresen un peso negativo
        peso=self.cleaned_data['peso']
        #si existe peso
        if peso:
            #si peso es = 0
            if peso==0:
                self.add_error('peso','Por favor ponga un peso valido')
            #si peso es menor a 0
            if peso<0:
                self.add_error('peso','por favor introduzca un numero positivo')

                
                    
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
            'objetivo'
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
        
        #pongo la info traida de los campos en variables
        edad=self.cleaned_data['edad']
        peso=self.cleaned_data['peso']


        #prevengo que ingresen un numero negativo en los campos
    
        if peso<=0:
            self.add_error('peso','Por favor introduzca un numero positivo')
        
        if edad<=0:
            self.add_error('edad','Por favor introduzca un numero positivo')
                
                
                
                    
        return cleaned_data
    
class AgregarNotaForm(forms.ModelForm):

    fecha=forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    

    class Meta:
        model=Nota
        fields=(
            'importancia',
            'texto',
        )



