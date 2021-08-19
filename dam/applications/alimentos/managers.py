from django.db import models

from django.db.models import Q


class AlimentoManager(models.Manager):
    #managers alimento

    def buscar_alimentos(self,kword):
        resultado= self.filter(
            Q(nombre__icontains=kword) | Q(marca__icontains=kword)
             
        )
        return resultado
    
    def buscar_alimentos_creadopor(self,usuario):
        resultado= self.filter(
            creada_por=usuario
             
        )
        return resultado
    

class AlimentoConsumidoManager(models.Manager):

    def buscar_alimentos_consumidos(self,kword):
        resultado=self.filter(
            diario=kword
        )
        return resultado
    
    def buscar_alimentos_consumidos_fk(self,kword):
        resultado=self.filter(
            diario=kword
        )
        return resultado
