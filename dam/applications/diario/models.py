from django.db import models

from .managers import DiarioManager
from applications.mascotas.models import Mascota

# Create your models here.

COMIDAS_CHOICES=(
    ('1','1'),
    ('2','2'),
    ('3','3'),
)

class Diario(models.Model):
    fecha=models.DateField(auto_now_add=False)
    mascota=models.ForeignKey(Mascota,on_delete=models.CASCADE)
    comidas=models.CharField(max_length=1,choices=COMIDAS_CHOICES,blank=True,default=2)
    total_cal=models.PositiveIntegerField(blank=True,null=True,default=0)

    dif_cal=models.IntegerField(blank=True,null=True,default=0)
    completado=models.BooleanField(default=False)

    class Meta:
        unique_together=(("fecha","mascota"),)

    objects=DiarioManager()

    def __str__(self):
        return str(self.id)+' '+str(self.fecha) +' '+ self.mascota.nombre

    
    

    




