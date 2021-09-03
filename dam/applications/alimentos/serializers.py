from rest_framework import serializers
from .models import Alimento

class AlimentoSerializer(serializers.ModelSerializer):

    class Meta:
        model=Alimento
        fields=(
            'id',
            'nombre',
            'marca',
            'calorias'
        )