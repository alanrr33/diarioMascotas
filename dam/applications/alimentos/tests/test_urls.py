from django.test import SimpleTestCase
#cuando las pruebas son simples y no requieren una db podemos usar simpletestcase
from django.urls import reverse,resolve
from applications.alimentos.views import (
                                        ListaAlimentos,
                                        BuscarAlimentos,
                                        AgregarAlimento,
                                        BorrarAlimento,
                                        EditarAlimento
                                        )

class TestUrls(SimpleTestCase):

    def test_listar_alimentos_is_resolved(self):
        url=reverse('alimentos_urls:listar-alimentos',args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, BuscarAlimentos)
    
    def test_lista_alimentos_is_resolved(self):
        url=reverse('alimentos_urls:listaalimentos')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, ListaAlimentos)
    

    def test_Agregar_Alimento_is_resolved(self):
        url=reverse('alimentos_urls:agregaralimento')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, AgregarAlimento)
    
    def test_Borrar_Alimento_is_resolved(self):
        url=reverse('alimentos_urls:eliminaralimento',args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, BorrarAlimento)

    def test_Editar_Alimento_is_resolved(self):
        url=reverse('alimentos_urls:editaralimento',args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, EditarAlimento)


    