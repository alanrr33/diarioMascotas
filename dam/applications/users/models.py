from django.db import models 
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin

from .managers import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES=(
        ('M','Masculino'),
        ('F','Femenino'),
        ('O','Otro'),
    )

    username=models.CharField(max_length=20,
                            unique=True,
                            validators=[ASCIIUsernameValidator(message='Ingrese un nombre de usuario valido.Letras, numeros, y los caracteres @/./+/-/_ ')],)
    email=models.EmailField()
    nombre=models.CharField(max_length=30,blank=True)
    apellido=models.CharField(max_length=30,blank=True)
    genero=models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    cod_registro=models.CharField(max_length=6, blank=True)

    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)

    USERNAME_FIELD='username'

    REQUIRED_FIELDS=['email',]

    objects=UserManager()

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.nombre + ' ' + self.apellido



