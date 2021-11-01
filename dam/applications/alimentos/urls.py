from django.urls import path
from .views import (
                    BuscarAlimentos,
                    ListaAlimentos,
                    AgregarAlimento,
                    BorrarAlimento,
                    EditarAlimento,
                    BuscarAlimentoListApiView,
                    AlimentoConsumidoListApiView,)

app_name="alimentos_urls"

urlpatterns = [
    path('listar-alimentos/<int:pk>/',BuscarAlimentos.as_view(),name="listar-alimentos"),
    path('lista-alimentos/',ListaAlimentos.as_view(),name="listaalimentos"),
    path('agregar-alimento/',AgregarAlimento.as_view(),name="agregaralimento"),
    path('eliminar-alimento/<int:pk>/',BorrarAlimento.as_view(),name="eliminaralimento"),
    path('editar-alimento/<int:pk>/',EditarAlimento.as_view(),name="editaralimento"),
    #apis
    path('api/alimentos/buscar/',BuscarAlimentoListApiView.as_view(),name="buscaralimentoapi"),
    path('api/alimentos-consumidos/buscar/',AlimentoConsumidoListApiView.as_view(),name="buscaralimentoconsumidoapi"),


]