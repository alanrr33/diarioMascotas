
from django.test.testcases import TestCase

from applications.alimentos.models import Alimento,AlimentoConsumido
from applications.users.models import User


class TestModel(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser('test_admin', '', 'test_admin')
        self.alimento1=Alimento.objects.create(
            id=1,
            nombre='alimento sabor pollo',
            marca='Whiskas',
            descripcion='Alimento sabor a pollo',
            calorias=1500,
            creada_por=self.user,
            tipo_mascota="Gato"

        )

    def test_alimento_str_concatena_id_nombre(self):
        self.assertEqual((str(self.alimento1)),'1 alimento sabor pollo')