from django.contrib import admin
from .models import (
                    Mascota,
                    PesoMascotaDiario,
                    Nota)

# Register your models here.

admin.site.register(Mascota)
admin.site.register(PesoMascotaDiario)
admin.site.register(Nota)
