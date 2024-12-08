from django.db import connection
from django.test import TestCase, Client

from main.utils_for_tests import create_groups_for_test, create_users_for_tests, create_doctors_for_tests, \
    create_appointments_for_tests
from services.models import Doctor, Appointment


class DoctorTestCase(TestCase):
    """Тестирование работоспособности контроллеров модели Doctor."""

    def reset_sequence(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE services_doctor_id_seq RESTART WITH 1;")

    def setUp(self):
        self.reset_sequence()

        self.user, self.other_user, self.medical_staff, self.other_medical_staff = create_users_for_tests(
            *create_groups_for_test()
        )

        self.doctor, self.others_doctor = create_doctors_for_tests(self.medical_staff, self.other_medical_staff)

        self.client = Client()
        self.client.force_login(user=self.medical_staff)

    def test_doctor_create(self):
        """Создание врача авторизованным пользователем."""

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
            "/services/doctor/create/"
        )

        self.assertTrue(Doctor.objects.filter(pk=3).exists())

    def test_doctor_list(self):
        """Просмотр списка врачей авторизованным пользователем."""

        response = self.client.get(
            '/services/doctor/list/',
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_doctor_detail(self):
        """Просмотр врача авторизованным пользователем."""

        response = self.client.get(
            '/services/doctor/detail/1/',
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_doctor_update(self):
        """Изменение врача авторизованным пользователем."""

        data = {
            "fullname": "change"
        }

        response = self.client.put(
            '/services/doctor/update/1/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_doctor_delete(self):
        """Удаление врача авторизованным пользователем."""

        response = self.client.delete(
            '/services/doctor/delete/1/'
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertEqual(
            response.url,
            "/services/doctor/list/"
        )

        self.assertTrue(not Doctor.objects.filter(pk=1).exists())


class AppointmentTestCase(TestCase):
    """Тестирование работоспособности контроллеров модели Appointment."""

    def reset_sequence(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE services_appointment_id_seq RESTART WITH 1;")

    def setUp(self):
        self.reset_sequence()

        self.user, self.other_user, self.medical_staff, self.other_medical_staff = create_users_for_tests(
            *create_groups_for_test()
        )

        self.appointment, self.others_appointment = create_appointments_for_tests(
            self.medical_staff, self.other_medical_staff
        )

        self.client = Client()
        self.client.force_login(user=self.medical_staff)

    def test_appointment_create(self):
        """Создание приема авторизованным пользователем."""

        data = {
            "title": "test",
            "treatment_room": 1
        }

        response = self.client.post(
            '/services/appointment/create/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertEqual(
            response.url,
            "/services/appointment/create/"
        )

        self.assertTrue(Appointment.objects.filter(pk=3))

    def test_appointment_list(self):
        """Просмотр списка приемов авторизованным пользователем."""

        response = self.client.get(
            '/services/appointment/list/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_appointment_detail(self):
        """Просмотр приема авторизованным пользователем."""

        response = self.client.get(
            '/services/appointment/detail/1/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_appointment_update(self):
        """Изменение приема авторизованным пользователем."""

        data = {
            "title": "change"
        }

        response = self.client.put(
            '/services/appointment/update/1/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_appointment_delete(self):
        """Удаление приема авторизованным пользователем."""

        response = self.client.delete(
            '/services/appointment/delete/1/'
        )

        self.assertEqual(
            response.status_code,
            302
        )

        self.assertEqual(
            response.url,
            "/services/appointment/list/"
        )

        self.assertTrue(not Appointment.objects.filter(pk=1))
