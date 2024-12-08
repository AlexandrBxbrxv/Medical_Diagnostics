from django.db import connection
from django.test import TestCase, Client

from main.utils_for_tests import create_groups_for_test, create_users_for_tests, create_doctors_for_tests, \
    create_appointments_for_tests
from services.models import Doctor, Appointment


class PermissionsForDoctorTestCase(TestCase):
    """Тестирование доступов к контроллерам модели Doctor."""

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

# Тесты доступов не авторизованного пользователя ####################
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

        self.assertTrue(not Doctor.objects.filter(pk=3).exists())

    def test_doctor_list_unauthorized(self):
        """Просмотр списка врачей неавторизованным пользователем."""

        response = self.client.get(
            '/services/doctor/list/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_doctor_detail_unauthorized(self):
        """Просмотр врача неавторизованным пользователем."""

        response = self.client.get(
            '/services/doctor/detail/1/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_doctor_update_unauthorized(self):
        """Изменение врача неавторизованным пользователем."""

        data = {
            "fullname": "change"
        }

        response = self.client.post(
            '/services/doctor/update/1/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_doctor_delete_unauthorized(self):
        """Удаление врача неавторизованным пользователем."""

        response = self.client.delete(
            '/services/doctor/delete/1/'
        )

        self.assertEqual(
            response.status_code,
            302
        )

# Тесты доступа авторизованного мед персонала к чужим объектам ######
    def test_doctor_detail_others_object(self):
        """Просмотр врача другого пользователя."""
        self.client.force_login(user=self.medical_staff)

        response = self.client.get(
            '/services/doctor/detail/2/'
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_doctor_update_others_object(self):
        """Изменение врача другого пользователя."""
        self.client.force_login(user=self.medical_staff)

        data = {
            "fullname": "change"
        }

        response = self.client.put(
            '/services/doctor/update/2/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_doctor_delete_others_object(self):
        """Изменение врача другого пользователя."""
        self.client.force_login(user=self.medical_staff)

        response = self.client.delete(
            '/services/doctor/delete/2/',
        )

        self.assertEqual(
            response.status_code,
            403
        )

# Тесты доступов авторизованного пользователя #######################
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

        self.assertTrue(not Doctor.objects.filter(pk=3).exists())

    def test_doctor_list_by_authorized_user(self):
        """Просмотр списка врачей авторизованным пользователем."""
        self.client.force_login(user=self.user)

        response = self.client.get(
            '/services/doctor/list/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_doctor_detail_by_authorized_user(self):
        """Просмотр врача авторизованным пользователем."""
        self.client.force_login(user=self.user)

        response = self.client.get(
            '/services/doctor/detail/1/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_doctor_update_by_authorized_user(self):
        """Изменение врача авторизованным пользователем."""
        self.client.force_login(user=self.user)

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
            403
        )

    def test_doctor_delete_by_authorized_user(self):
        """Удаление врача авторизованным пользователем."""
        self.client.force_login(user=self.user)

        response = self.client.delete(
            '/services/doctor/delete/1/',
        )

        self.assertEqual(
            response.status_code,
            403
        )


class PermissionsForAppointmentTestCase(TestCase):
    """Тестирование доступов к контроллерам модели Appointment."""

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

# Тесты доступов не авторизованного пользователя ####################
    def test_appointment_create_unauthorized(self):
        """Создание приема неавторизованным пользователем."""
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
            "/users/login/?next=/services/appointment/create/"
        )

        self.assertTrue(not Appointment.objects.filter(pk=3).exists())

    def test_appointment_list_unauthorized(self):
        """Просмотр списка приемов неавторизованным пользователем."""

        response = self.client.get(
            '/services/appointment/list/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_appointment_detail_unauthorized(self):
        """Просмотр приема неавторизованным пользователем."""

        response = self.client.get(
            '/services/appointment/detail/1/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_appointment_update_unauthorized(self):
        """Изменение приема неавторизованным пользователем."""

        data = {
            "title": "change"
        }

        response = self.client.post(
            '/services/appointment/update/1/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            302
        )

    def test_appointment_delete_unauthorized(self):
        """Удаление приема неавторизованным пользователем."""

        response = self.client.delete(
            '/services/appointment/delete/1/'
        )

        self.assertEqual(
            response.status_code,
            302
        )

# Тесты доступа авторизованного мед персонала к чужим объектам ######
    def test_appointment_detail_others_object(self):
        """Просмотр приема другого пользователя."""
        self.client.force_login(user=self.medical_staff)

        response = self.client.get(
            '/services/appointment/detail/2/'
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_appointment_update_others_object(self):
        """Изменение приема другого пользователя."""
        self.client.force_login(user=self.medical_staff)

        data = {
            "title": "change"
        }

        response = self.client.put(
            '/services/appointment/update/2/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            403
        )

    def test_appointment_delete_others_object(self):
        """Изменение приема другого пользователя."""
        self.client.force_login(user=self.medical_staff)

        response = self.client.delete(
            '/services/appointment/delete/2/',
        )

        self.assertEqual(
            response.status_code,
            403
        )

# Тесты доступов авторизованного пользователя #######################
    def test_appointment_create_by_authorized_user(self):
        """Создание приема авторизованным пользователем."""
        self.client.force_login(user=self.user)

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
            403
        )

        self.assertTrue(not Appointment.objects.filter(pk=3).exists())

    def test_appointment_list_by_authorized_user(self):
        """Просмотр списка приемов авторизованным пользователем."""
        self.client.force_login(user=self.user)

        response = self.client.get(
            '/services/appointment/list/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_appointment_detail_by_authorized_user(self):
        """Просмотр приема авторизованным пользователем."""
        self.client.force_login(user=self.user)

        response = self.client.get(
            '/services/appointment/detail/1/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_appointment_update_by_authorized_user(self):
        """Изменение приема авторизованным пользователем."""
        self.client.force_login(user=self.user)

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
            403
        )

    def test_appointment_delete_by_authorized_user(self):
        """Удаление приема авторизованным пользователем."""
        self.client.force_login(user=self.user)

        response = self.client.delete(
            '/services/appointment/delete/1/',
        )

        self.assertEqual(
            response.status_code,
            403
        )
