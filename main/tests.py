import datetime

from django.db import connection
from django.test import TestCase, Client

from main.models import Feedback
from users.models import User


class MainAppTestCase(TestCase):
    """Тестирование работоспособности контроллеров приложения main"""

    def reset_sequence(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE main_feedback_id_seq RESTART WITH 1;")

    def setUp(self):
        self.date_time = datetime.datetime.now()

        self.user = User.objects.create(
            email='user@test.ru',
            fullname='Фамилия Имя Отчество',
            phone_number='+77777777771',
            password='test'
        )

        self.client = Client()

    def test_index_unauthorized(self):
        """Доступ к странице 'Главная' без авторизации."""
        response = self.client.get(
            ''
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_index(self):
        """Доступ к странице 'Главная' авторизованным пользователем."""
        self.client.force_login(user=self.user)

        response = self.client.get(
            ''
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_about_unauthorized(self):
        """Доступ к странице 'О компании' без авторизации."""
        response = self.client.get(
            '/about/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_about(self):
        """Доступ к странице 'О компании' авторизованным пользователем."""
        self.client.force_login(user=self.user)

        response = self.client.get(
            '/about/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_contacts_unauthorized(self):
        """Доступ к странице 'Контакты' без авторизации."""
        response = self.client.get(
            '/contacts/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_contacts(self):
        """Доступ к странице 'Контакты' авторизованным пользователем."""
        self.client.force_login(user=self.user)

        response = self.client.get(
            '/contacts/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_feedback_unauthorized(self):
        """Тестирование работоспособности формы обратной связи без авторизации."""
        data = {
            "fullname": "test test test",
            "email": "test@te.st",
            "message": "test"
        }

        response = self.client.post(
            '/feedback/?page=index',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            200
        )

        feedback = Feedback.objects.all().first()
        self.assertEqual(
            {
                'date_created': feedback.date_created,
                'email': feedback.email,
                'fullname': feedback.fullname,
                'id': feedback.id,
                'is_closed': feedback.is_closed,
                'message': feedback.message,
                'owner_id': feedback.owner_id,
            },
            {
                'date_created': self.date_time.date(),
                'email': 'test@te.st',
                'fullname': 'test test test',
                'id': 2,
                'is_closed': False,
                'message': 'test',
                'owner_id': None
            }
        )

    def test_feedback(self):
        """Тестирование работоспособности формы обратной связи авторизованным пользователем."""
        self.client.force_login(user=self.user)

        data = {
            "fullname": "test test test",
            "email": "test@te.st",
            "message": "test"
        }

        response = self.client.post(
            '/feedback/?page=contacts',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            200
        )

        feedback = Feedback.objects.all().first()
        self.assertEqual(
            {
                'date_created': feedback.date_created,
                'email': feedback.email,
                'fullname': feedback.fullname,
                'id': feedback.id,
                'is_closed': feedback.is_closed,
                'message': feedback.message,
                'owner_id': feedback.owner_id,
            },
            {
                'date_created': self.date_time.date(),
                'email': 'test@te.st',
                'fullname': 'test test test',
                'id': 1,
                'is_closed': False,
                'message': 'test',
                'owner_id': 5
            }
        )
