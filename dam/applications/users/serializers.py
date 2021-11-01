from rest_framework import serializers
from .models import User

class DueñoSerializer(serializers.ModelSerializer):
    id=serializers.IntegerField()
    nombre=serializers.CharField()
    apellido=serializers.CharField()

    class Meta:
        model=User
        fields=(
            'id',
            'nombre',
            'apellido'
        )