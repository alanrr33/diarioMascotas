from rest_framework import serializers
from .models import Mascota
from applications.users.serializers import DueñoSerializer

class MascotaSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField()
    #dueño=DueñoSerializer()
    nombre=serializers.CharField()
    tipo=serializers.CharField()
    peso=serializers.IntegerField()

    class Meta:
        model=Mascota
        fields=(
            'id',
            'dueño',
            'nombre',
            'tipo',
            'peso'
        )