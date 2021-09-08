from django import forms
from .models import AlimentoConsumido,Alimento

class BusquedaForm(forms.Form):
    
    busqueda = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs = {
                'placeholder': 'Ingrese busqueda aqui',
                'class': 'input-group-field',
            }
        )
    )

class EditarAlimentoForm(forms.ModelForm):
    class Meta:
        #modelo al que se conecta
        model=Alimento
        fields=(
            'nombre',
            'marca',
            'descripcion',
            'calorias',    
        )

    def __init__(self, *args, **kwargs):
        #saco el id de los kwargs
        alimentoid=kwargs.pop('pk','')
        #llamamos al constructor de la clase padre
        super(EditarAlimentoForm, self).__init__(*args, **kwargs)
        #y podemos acceder a las propiedades de los campos
      
        alimento=Alimento.objects.get(pk=alimentoid)
        self.fields['nombre'].initial=alimento.nombre
        self.fields['marca'].initial=alimento.marca
        self.fields['descripcion'].initial=alimento.descripcion
        self.fields['calorias'].initial=alimento.calorias


class DiarioForm(forms.ModelForm):
    class Meta:
        #modelo al que se conecta
        model=AlimentoConsumido
        fields=('id',)



