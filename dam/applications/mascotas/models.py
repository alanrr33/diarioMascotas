from decimal import Decimal

from django.db import models
from django.db.models.signals import post_save

from .managers import MascotaManager
from applications.users.models import User

# Create your models here.

class Mascota(models.Model):

    TIPO_CHOICES=(
        ('Gato','Gato'),
        ('Perro','Perro'),
    )

    ACTIVIDAD_CHOICES=(
        ('Poca','Poca'),
        ('Normal','Normal'),
        ('Moderada','Moderada'),
        ('Intensa','Intensa'),
    )

    TAMAÑO_CHOICES=(
        ('Muy pequeño','Muy pequeño'),
        ('Pequeño','Pequeño'),
        ('Mediano','Mediano'),
        ('Grande','Grande'),
        ('Gigante','Gigante'),
    )

    OBJETIVO_CHOICES=(
        ('Bajar peso','Bajar peso'),
        ('Mantener peso','Mantener peso'),
        ('Aumentar peso','Aumentar peso'),
    )

    class Meta:
        ordering=['id']



    #configuración basica
    dueño=models.ForeignKey(User,on_delete=models.CASCADE)
    nombre=models.CharField(max_length=30,blank=False)
    tipo=models.CharField(max_length=5,choices=TIPO_CHOICES,blank=False)
    peso=models.DecimalField(max_digits=4,decimal_places=2,help_text="Peso en Kg")
    #edad en meses
    edad=models.PositiveIntegerField(default=12,help_text="Edad en meses")
    actividad=models.CharField(max_length=10,choices=ACTIVIDAD_CHOICES,default="Poca",blank=False)
    #meta calorias
    meta=models.PositiveIntegerField('Meta calorias',null=True)
    tamaño=models.CharField(max_length=15,choices=TAMAÑO_CHOICES,blank=False,default="Mediano")
    esterilizado=models.BooleanField(default=False,help_text="Tildado = Si")
    objetivo=models.CharField(max_length=15,choices=OBJETIVO_CHOICES, default="Mantener peso")
    imagen=models.ImageField('Imagen',upload_to='Imgmascotas/',blank=True)

  

    #le indicamos que el nuevo manager va a ser el que importamos localmente
    objects=MascotaManager()

    def __str__(self):
        return str(self.id)+' '+self.nombre

    def imprimir(self):
        print ('jajajajsdxd')

class PesoMascotaDiario(models.Model):

    class Meta:
        ordering=['id','fecha']
        unique_together=['mascota','fecha']

    mascota=models.ForeignKey(Mascota,on_delete=models.CASCADE)
    peso=models.DecimalField(max_digits=4,decimal_places=2,help_text="Peso en Kg")
    fecha=models.DateField(auto_now_add=False)
    

    def __str__(self):
        return str(self.id)+' '+self.mascota.nombre

class Nota(models.Model):

    IMPORTANCIA_CHOICES=(
        ('Normal','Normal'),
        ('Moderada','Moderada'),
        ('Alta','Alta'),
    )

    class Meta:
        ordering=['id']

    mascota=models.ForeignKey(Mascota,on_delete=models.CASCADE)
    fecha=models.DateField(auto_now_add=False)
    importancia=models.CharField(max_length=8,choices=IMPORTANCIA_CHOICES,blank=False)
    texto=models.CharField(max_length=200,blank=False,default="Nota")

    def __str__(self):
        return str(self.id)+' '+self.mascota.nombre
    

    


def calc_meta(sender,instance,**kwargs):

    if instance.tipo=="Gato":
        print("soy gato")
        print('peso '+str(instance.peso)) 

        #objetivo default mant peso,
        #despues ajustar val necesarios
        #acorde objetivo alcanzar

        if instance.edad>=12:
            print('soy gato adulto')
            if instance.esterilizado==True:
                mult=1.2
                if instance.actividad=="Normal" or instance.actividad =="Moderada":
                    mult+=0
                if instance.actividad=="Poca":
                    print('poca actividad')
                    mult-=0.2 

            if instance.esterilizado==False:
                mult=1.4
                print('no estoy esterilizado')
                if instance.actividad=="Normal" or instance.actividad =="Moderada":
                    mult+=0
                if instance.actividad=="Poca":
                    print('poca actividad')
                    mult-=0.4   

        if instance.edad<12:
            print('soy cachorro')
            if 0 <= instance.edad < 4:
                print('entre 0 y 4')
                mult=2.5
            if 4 <= instance.edad <12:
                print('entre 4 y 12')
                mult=2
        #hasta aca todo joya

        ner=70*(pow(Decimal(instance.peso), Decimal(0.75)))
        mer=round(ner*Decimal(mult) , 2)
        print(mult)
        print(ner)
        print(mer)
        Mascota.objects.filter(id=instance.id).update(meta=mer)


    if instance.tipo=="Perro":
        print("soy perro")
        print('peso '+str(instance.peso))
        
        if instance.edad>=12:
            print('soy perro adulto')
            if instance.esterilizado==True:
                mult=1.6
                print('estoy esterilizado')
                if instance.actividad=="Poca":
                    mult+=0
                if instance.actividad=="Normal":
                    mult+=0.4
                if instance.actividad=="Moderada":
                    mult+=1.4
                if instance.actividad=="Intensa":
                    mult+=4.4

            if instance.esterilizado==False:
                print('no estoy esterilizado')
                mult=1.8
                print('estoy esterilizado')
                if instance.actividad=="Poca":
                    mult+=0
                if instance.actividad=="Normal":
                    mult+=0.2
                if instance.actividad=="Moderada":
                    mult+=1.2
                if instance.actividad=="Intensa":
                    mult+=4.2

        if instance.edad<12:
            print('soy cachorro')
            if 0 <= instance.edad < 4:
                print('entre 0 y 4')
                mult=3
            if 4 <= instance.edad <12:
                print('entre 4 y 12')
                mult=2
        #hasta aca todo joya

        ner=70*(pow(Decimal(instance.peso), Decimal(0.75)))
        mer=round(ner*Decimal(mult) , 0)
        print(mult)
        print(ner)
        print(mer)
        Mascota.objects.filter(id=instance.id).update(meta=mer)

post_save.connect(calc_meta,sender=Mascota)
