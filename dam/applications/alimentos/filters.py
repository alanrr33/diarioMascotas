import django_filters
from django.db.models import Q

from .models import Alimento

class AlimentoFilter(django_filters.FilterSet):



    Busqueda = django_filters.CharFilter(label='Buscar',method='buscar_por_nombre_y_marca')

    class Meta:
        model=Alimento
        fields=['Busqueda']
    
    def buscar_por_nombre_y_marca(self, queryset, name, value):

        return Alimento.objects.filter(
            Q(nombre__icontains=value) | Q(marca__icontains=value) 
        )


