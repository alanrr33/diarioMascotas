from django.urls import path

from .views import (
                    VerDiarios,
                    EditarAlimentoDiario,
                    EliminarAlimentoDiario,
                    DetalleDiario,
                    BuscarDiarioApiView
                    )


app_name="diario_urls"

urlpatterns = [
    #path('mostrar/',,name="mostrar-mascotas"),
    path('ver-diarios/<pk>/',VerDiarios.as_view(),name="verdiario"),
    path('detalle-diario/<pk>/',DetalleDiario.as_view(),name="detallediario"),
    path('editar-alimento/<pk>/',EditarAlimentoDiario.as_view(),name="editalimento"),
    path('eliminar-alimento/<pk>/',EliminarAlimentoDiario.as_view(),name="eliminaralimento"),
    path('api/diarios/buscar/',BuscarDiarioApiView.as_view(),name="buscardiario"),

]
