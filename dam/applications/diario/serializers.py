from rest_framework import serializers
from .models import Diario
from applications.mascotas.serializers import MascotaSerializer

class DiarioSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField()
    fecha=serializers.CharField()
    #mascota=MascotaSerializer()
    total_cal=serializers.IntegerField()

    class Meta:
        model=Diario
        fields=(
            'id',
            'fecha',
            'mascota',
            'total_cal'
        )