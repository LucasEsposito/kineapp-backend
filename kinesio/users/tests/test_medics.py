from kinesioapp.utils.test_utils import APITestCase
from rest_framework import status

from ..models import User


class TestMedicsAPI(APITestCase):
    def setUp(self) -> None:
        self.medic = User.objects.create_user(username='juan', password='1234', license='matricula #15433')
        User.objects.create_user(username='maria22', license='matricula #44423')
        self._log_in(self.medic, '1234')

    def test_get_all_medics(self):
        response = self.client.get('/api/v1/medics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['data']), 2)

    def test_update_medic_first_name(self):
        data = {'first_name': 'raul'}
        response = self.client.patch('/api/v1/medics/detail', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check the response
        self.assertEqual(response.json()['first_name'], 'raul')
        # Check whether the db was properly updated or not
        self.medic.refresh_from_db()
        self.assertEqual(self.medic.first_name, 'raul')

    def test_update_one_medic_license(self):
        self._log_in(self.medic, '1234')
        data = {'medic': {'license': 'new license'}}
        response = self.client.patch('/api/v1/medics/detail', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check the response
        self.assertEqual(response.json()['medic']['license'], 'new license')
        # Check whether the db was properly updated or not
        self.medic.refresh_from_db()
        self.assertEqual(self.medic.medic.license, 'new license')

    # def test_dont_see_id_on_get(self): Set question on SetUp and fix this test (get secret_question, not *_id)
    #     response = self.client.get('/api/v1/medics/')
    #     self.assertEqual(response.json().get('data')[0].get('id', None), None)
