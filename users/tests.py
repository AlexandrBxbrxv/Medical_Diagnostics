from django.db import connection
from django.test import TestCase, Client

from main.utils_for_tests import create_groups_for_test, create_users_for_tests, create_carts_for_tests, \
    create_histories_for_tests
from services.models import Analysis


class CartTestCase(TestCase):
    """Тестирование работоспособности контроллеров модели Cart."""

    def reset_sequence(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE users_cart_id_seq RESTART WITH 1;")

    def setUp(self):
        self.reset_sequence()

        self.user, self.other_user, self.medical_staff, self.other_medical_staff = create_users_for_tests(
            *create_groups_for_test()
        )

        self.cart, self.others_cart = create_carts_for_tests(self.user, self.other_user)

        self.client = Client()
        self.client.force_login(user=self.user)

    def test_cart_list(self):
        """Просмотр списка корзин авторизованным пользователем."""

        response = self.client.get(
            '/users/cart/',
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_add_to_cart(self):
        """Добавление анализа в корзину."""

        analysis_3 = Analysis.objects.create(
            owner=self.medical_staff,
            title='test',
            description='test',
            preparation='test',
            treatment_room=1,
            price=1
        )

        data = {"type": "analysis", "id": analysis_3.pk}

        response = self.client.get(
            '/users/add_to_cart/',
            data=data

        )

        self.assertEqual(
            response.status_code,
            201
        )

    def test_delete_from_cart(self):
        """Удаление объекта из корзины."""

        data = {"id": 1}

        response = self.client.get(
            '/users/delete_from_cart/',
            data=data

        )

        self.assertEqual(
            response.status_code,
            204
        )


class HistoryTestCase(TestCase):
    """Тестирование работоспособности контроллеров модели History."""

    def reset_sequence(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE users_history_id_seq RESTART WITH 1;")

    def setUp(self):
        self.reset_sequence()

        self.user, self.other_user, self.medical_staff, self.other_medical_staff = create_users_for_tests(
            *create_groups_for_test()
        )

        self.history, self.others_history = create_histories_for_tests(self.user, self.other_user)

        self.client = Client()
        self.client.force_login(user=self.user)

    def test_history_list(self):
        """Просмотр списка истории авторизованным пользователем."""

        response = self.client.get(
            '/users/history/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_history_detail(self):
        """Просмотр объекта истории авторизованным пользователем."""

        response = self.client.get(
            '/users/history/detail/1/'
        )

        self.assertEqual(
            response.status_code,
            200
        )
