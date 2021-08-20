from decimal import Decimal
from django.db import models

class MascotaManager(models.Manager):


    def _create_mascota(self,dueño,nombre,tipo,edad,peso,actividad,tamaño,esterilizado,objetivo):
        #hacemos un llamado al model que esta usando este manager
        mascota=self.model(
            dueño=dueño,
            nombre=nombre,
            tipo=tipo,
            edad=edad,
            peso=peso,
            actividad=actividad,
            tamaño=tamaño,
            esterilizado=esterilizado,
            objetivo=objetivo,
            
            )
        #le indicamos que se guarde utilizando la db actual
        mascota.save(using=self.db)
        #imprimo por las dudas
        print("Añadiendo mascota {} a {}".format(mascota,dueño))
        return mascota

    def create_mascota(self,dueño,nombre,tipo,edad,peso,actividad,tamaño,esterilizado,objetivo):
        return self._create_mascota(dueño,nombre,tipo,edad,peso,actividad,tamaño,esterilizado,objetivo)

    def buscar_mascota_dueñoid(self,kword):
        resultado= self.filter(
            dueño__id=kword
        )
        print(resultado)
        return resultado

    