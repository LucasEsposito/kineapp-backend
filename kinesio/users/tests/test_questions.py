from kinesioapp.utils.test_utils import APITestCase
from rest_framework import status
from kinesio import settings
from django.utils import timezone

from ..models import User, SecretQuestion


class TestQuestionsAPI(APITestCase):
    def setUp(self) -> None:
        self.question = SecretQuestion.objects.create(description='Cual es tu comida favorita?')
        SecretQuestion.objects.create(description='Como se llama tu perro?')

    def test_get_all_questions(self):
        response = self.client.get('/api/v1/secret_questions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('data')), 2)


class CheckAnswerAPI(APITestCase):
    def setUp(self) -> None:
        self.question = SecretQuestion.objects.create(description='Cual es tu color favorito?')
        self.user = User.objects.create_user(username='2429231164242114344333', secret_question_id=self.question.id,
                                             dni=39203040, birth_date=timezone.now())
        self.user.set_password('rojo')
        self.user.save()

    def test_check_valid_question_answer(self):
        response = self.client.post('/api/v1/login/', {
            "google_token": self.user.username,
            "secret_question_id": self.question.id,
            "answer": "rojo"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'Ha iniciado sesión correctamente.')

    def test_check_wrong_question_answer(self):
        response = self.client.post('/api/v1/login/', {
            "google_token": self.user.username,
            "secret_question_id": self.question.id,
            "answer": "azul"
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token(self):
        self.user.delete()
        response = self.client.post('/api/v1/login/', {
            "google_token": "random invalid token",
            "secret_question_id": self.question.id,
            "answer": "rojo"
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_question_id_not_found(self):
        response = self.client.post('/api/v1/login/', {
            "google_token": self.user.username,
            "secret_question_id": 879879,
            "answer": "rojo"
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_fail_max_times(self):
        for x in range(0, int(settings.MAX_PASSWORD_TRIES) + 1):
            response = self.client.post('/api/v1/login/', {
                "google_token": self.user.username,
                "secret_question_id": self.question.id,
                "answer": "negro"
            })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json().get("message"), "Su cuenta ha sido bloqueada por superar el límite de accesos incorrectos.")
