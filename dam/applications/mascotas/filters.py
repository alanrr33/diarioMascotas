import django_filters
from django_filters.widgets import RangeWidget

from .models import Nota

class NotaFilter(django_filters.FilterSet):

    IMP_CHOICES=(
        ('Normal','Normal'),
        ('Moderada','Moderada'),
        ('Alta','Alta')
    )

    CHOICES=(
        ('ascendente','Ascendente'),
        ('descendente','Descendente')
    )


    importancia=django_filters.ChoiceFilter(field_name='importancia',choices=IMP_CHOICES)
    fecha = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'type': 'date'}))
    orden=django_filters.ChoiceFilter(label='Orden',choices=CHOICES,method='filtrar_por_orden')

    class Meta:
        model=Nota
        fields=['fecha','importancia']
    
    def filtrar_por_orden(self,queryset,name,value):

        orden= 'fecha' if value=='ascendente' else '-fecha'

        return queryset.order_by(orden)