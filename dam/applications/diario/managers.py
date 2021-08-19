from django.db import models



class DiarioManager(models.Manager):
    #managers alimento

    def buscar_diarios(self,kword):
        resultado= self.filter(
            mascota=kword
             
        ).order_by('-fecha')
        return resultado

        