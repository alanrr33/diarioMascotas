from django.db import models
from django.db.models.signals import post_delete,post_save,pre_save

from applications.users.models import User
from applications.diario.models import Diario
from .managers import AlimentoManager,AlimentoConsumidoManager



class Alimento(models.Model):
    nombre=models.CharField(max_length=50,blank=False)
    marca=models.CharField(max_length=50,blank=False)
    descripcion=models.CharField(max_length=70,blank=False)
    #numeros hasta 999 con 2 posiciones decimales
    calorias=models.PositiveIntegerField(blank=False,help_text="por kg")
    creada_por=models.ForeignKey(User,on_delete=models.CASCADE)
    creada_el=models.DateField(auto_now_add=True)


    objects=AlimentoManager()


    def __str__(self):
        return str(self.id)+' '+self.nombre


PORCION_CHOICES=(
    ('1','1'),
    ('100','100'),
)
    
class AlimentoConsumido(models.Model):
    alimento=models.ForeignKey(Alimento,on_delete=models.CASCADE)
    diario=models.ForeignKey(Diario,on_delete=models.CASCADE)
    cantidad=models.PositiveIntegerField()
    porcion=models.CharField(max_length=10,choices=PORCION_CHOICES,default="1g",help_text="Gramos")
    total_cal=models.PositiveIntegerField()

    objects=AlimentoConsumidoManager()

    def __str__(self):
        return str(self.id)+' '+self.alimento.nombre

    def limpiar_lista(lista):
        lista_clean=[]
        for i in lista:
                if i:
                    lista_clean.append(i)
        return lista_clean
    
def update_total_cal_borrar(sender,instance,**kwargs):
    #actualizamos total calorias al borrar alimento
    print('update total calorias despues de borrar alimento')
    instance.diario.total_cal-=instance.total_cal
    instance.diario.save()


def update_calorias_alimento_consumido(sender,instance,**kwargs):
    #actualizamos las calorias del alimento al ser actualizado

    calorias_gramo=(int((instance.alimento.calorias)/1000))
    nuevo_total_cal=(
        ((int(instance.cantidad))*(int(instance.porcion))*calorias_gramo)

        )
    AlimentoConsumido.objects.filter(pk=instance.pk).update(total_cal=nuevo_total_cal)

    alimentos=AlimentoConsumido.objects.buscar_alimentos_consumidos(instance.diario)
    caloriastotal=0
    for i in alimentos:
        print('alimento: {}'.format(i))
        caloriastotal+=i.total_cal
    
    instance.diario.total_cal=caloriastotal
    instance.diario.save()

    print('update calorias totales')



post_delete.connect(update_total_cal_borrar,sender=AlimentoConsumido)
post_save.connect(update_calorias_alimento_consumido,sender=AlimentoConsumido)



        

    



    

