from django.db import connection
from django.test import TestCase, Client

from main.utils_for_tests import create_groups_for_test, create_users_for_tests
from services.models import Doctor


class PermissionTestCase(TestCase):
    """Тестирование доступов к контроллерам."""

    def reset_sequence(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE services_doctor_id_seq RESTART WITH 1;")

    def setUp(self):
        self.reset_sequence()

        self.user, self.other_user, self.medical_staff, self.other_medical_staff = create_users_for_tests(
            *create_groups_for_test()
        )

        self.client = Client()

    def test_doctor_create_unauthorized(self):
        """Создание врача неавторизованным пользователем."""
        data = {
            "fullname": "Фамилия Имя Отчество",
            "speciality": "test",
            "education": "test",
            "experience": 3
        }

        response = self.client.post(
            '/services/doctor/create/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertEqual(
            response.url,
            "/users/login/?next=/services/doctor/create/"
        )

        self.assertTrue(not Doctor.objects.filter(pk=1).exists())

    def test_doctor_list_unauthorized(self):
        """Просмотр списка врачей неавторизованным пользователем."""

        response = self.client.get(
            '/services/doctor/list/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_doctor_create_by_authorized_user(self):
        """Создание врача авторизованным пользователем."""
        self.client.force_login(user=self.user)

        data = {
            "fullname": "Фамилия Имя Отчество",
            "speciality": "test",
            "education": "test",
            "experience": 3
        }

        response = self.client.post(
            '/services/doctor/create/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            403
        )

        self.assertTrue(not Doctor.objects.filter(pk=1).exists())

