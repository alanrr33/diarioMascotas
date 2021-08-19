from django import forms
from .models import Diario
from applications.alimentos.models import AlimentoConsumido


class BusquedaForm(forms.ModelForm):
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
        model=AlimentoConsumido
        fields=(
            'cantidad',
            'porcion',    
        )



    def __init__(self, *args, **kwargs):
        #saco el id de los kwargs
        alimentoid=kwargs.pop('pk','')
        #llamamos al constructor de la clase padre
        super(EditarAlimentoForm, self).__init__(*args, **kwargs)
        #y podemos acceder a las propiedades de los campos
        alimento=AlimentoConsumido.objects.get(pk=alimentoid)
        self.fields['cantidad'].required = True
        self.fields['porcion'].required=True
        self.fields['cantidad'].initial=alimento.cantidad
        self.fields['porcion'].initial=alimento.porcion
        


class CompletarDiarioForm(forms.ModelForm):
    class Meta:
        #modelo al que se conecta
        model=Diario
        fields=('id',)

