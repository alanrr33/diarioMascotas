from django.urls import path
from .views import (MascotaRegisterView,
                    ListarMascotasView,
                    UpdateMascotaView,
                    DeleteMascotaView,
                    PanelMascotaView,
                    ReportesMascotaView,
                    listresults)

app_name="mascotas_urls"

urlpatterns = [
    path('registrar/',MascotaRegisterView.as_view(),name="registrarmascota"),
    path('listar-mascotas/',ListarMascotasView.as_view(),name="listarmascotas"),
    path('editar/<int:pk>/',UpdateMascotaView.as_view(),name="editar"),
    path('panel-mascota/<int:pk>/',PanelMascotaView.as_view(),name="panelmascota"),
    path('eliminar-mascotas/<int:pk>/',DeleteMascotaView.as_view(),name="delete"),
    path('reportes-mascotas/<int:pk>/',ReportesMascotaView.as_view(),name="reportes"),
    #path('descargar/',listresults,name="descargar"),
    path('descargar/<int:pk>/',listresults,name="descargar"),


]