
from datetime import datetime
from django.http import response
from django.test.testcases import TestCase,Client
from django.urls import reverse
from applications.alimentos.models import Alimento,AlimentoConsumido
from applications.diario.models import Diario
from applications.users.models import User
from applications.mascotas.models import Mascota
import json

class TestViews(TestCase):

    def setUp(self):
        self.client=Client()

        #login
        self.user = User.objects.create_superuser('test_admin', '', 'test_admin')
        self.user2=User.objects.create_user('test_user','','test_user')
        self.client.login(username='test_admin', password='test_admin')

        #urls
        self.list_alimento_url=reverse('alimentos_urls:listaalimentos')
        self.listar_alimentos_url=reverse('alimentos_urls:listar-alimentos',args=[1])
        self.agregar_alimento_url=reverse('alimentos_urls:agregaralimento')
        self.borrar_alimento_url=reverse('alimentos_urls:eliminaralimento',args=[1])

        #objetos falsos
        self.mascota=Mascota.objects.create(id=1,dueño=self.user,peso=20)
        self.diario=Diario.objects.create(id=1,fecha=datetime.today(),mascota_id=1)
        




    def test_list_alimento_GET(self):

        response=self.client.get(self.list_alimento_url)  
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'alimentos/lista_alimentos.html')

    def test_listar_alimentos_GET(self):

        #self.diario=Diario.objects.create(datetime.now(),1)
        response=self.client.get(self.listar_alimentos_url)  
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'alimentos/buscar_alimento.html')

    

    def test_agregar_alimento_POST_agrega_nuevo_alimento(self):

        response=self.client.post(self.agregar_alimento_url,{
            'nombre':'alimento sabor pollo',
            'marca':'Whiskas',
            'descripcion':'Alimento sabor a pollo',
            'calorias':1500,
            'creada_por':self.user,
            'tipo_mascota':"Gato"


        })

        #nos tiene que devolver un redirect al crearse el objeto
        self.assertEqual(response.status_code,302)
        #una vez creado confirmamos que se creo con los datos que pasamos
        self.assertEqual(Alimento.objects.first().nombre,'alimento sabor pollo')
    
    def test_agregar_alimento_POST_sin_data(self):

        response=self.client.post(self.agregar_alimento_url)

        self.assertEqual(response.status_code,200)
        self.assertEqual(Alimento.objects.count(),0)

    def test_BorrarAlimento_GET_borra_alimento_si_creada_por_igual_user(self):

        Alimento.objects.create(
            id=1,
            nombre='alimento sabor pollo',
            marca='Whiskas',
            descripcion='Alimento sabor a pollo',
            calorias=1500,
            creada_por=self.user,
            tipo_mascota="Gato"
        )
        response=self.client.get(self.borrar_alimento_url)

        self.assertEqual(response.status_code,302)
        self.assertEqual(Alimento.objects.count(),0)
    
    def test_BorrarAlimento_GET_borra_alimento_si_creada_por_distinto_user(self):

        Alimento.objects.create(
            id=1,
            nombre='alimento sabor pollo',
            marca='Whiskas',
            descripcion='Alimento sabor a pollo',
            calorias=1500,
            creada_por=self.user2,
            tipo_mascota="Gato"
        )
        response=self.client.get(self.borrar_alimento_url)

        self.assertEqual(response.status_code,302)
        #el conteo de la db debería devolver 1 porque no puede ser borrado si no es por el usuario que lo creo
        self.assertEqual(Alimento.objects.count(),1)
    

    def test_EditarAlimento_POST_edita_alimento_si_creada_por_igual_user(self):

        alimento=Alimento.objects.create(
            nombre='alimento sabor pollo',
            marca='Whiskas',
            descripcion='Alimento sabor a pollo',
            calorias=1500,
            creada_por=self.user,
            tipo_mascota="Gato"
        )

        response = self.client.post(
            reverse('alimentos_urls:editaralimento', kwargs={'pk': alimento.id}), 
            {
             'nombre':'alimento sabor carne',
             'marca':'Cat chow',
             'descripcion':'miau',
             'calorias':0

            })


        self.assertEqual(response.status_code,302)
        alimento.refresh_from_db()
        
        #el conteo de la db debería devolver 1 porque no puede ser borrado si no es por el usuario que lo creo
        self.assertEqual(Alimento.objects.first().nombre,'alimento sabor carne')
        self.assertEqual(Alimento.objects.first().marca,'Cat chow')

    


    
    




        
