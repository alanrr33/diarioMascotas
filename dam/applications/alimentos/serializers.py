from rest_framework import serializers
from .models import Alimento,AlimentoConsumido


class AlimentoSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField()
    nombre=serializers.CharField()
    marca=serializers.CharField()
    calorias=serializers.IntegerField()

    class Meta:
        model=Alimento
        fields=(
            'id',
            'nombre',
            'marca',
            'calorias'
        )

class AlimentoConsumidoSerializer(serializers.ModelSerializer):

    #alimento=AlimentoSerializer()
    
    class Meta:
        model=AlimentoConsumido
        fields=(
            'id',
            'alimento',
            'diario',
            'cantidad',
            'total_cal'
        )