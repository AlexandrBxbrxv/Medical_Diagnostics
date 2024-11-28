# Эти функции для импорта в setUp метод в тестах

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from services.models import Doctor
from users.models import User


def create_groups_for_test() -> tuple:
    """Создает и заполняет группы для тестов. Возвращает: user_group, medical_staff_group"""
    medical_staff_group = Group.objects.create(name='medical_staff')
    user_group = Group.objects.create(name='user')

    # permissions for Doctor ############################################
    content_type_doctor = ContentType.objects.get_for_model(Doctor)

    add_doctor = Permission.objects.get(
        codename='add_doctor',
        content_type=content_type_doctor,
    )

    view_doctor = Permission.objects.get(
        codename='view_doctor',
        content_type=content_type_doctor,
    )

    change_doctor = Permission.objects.get(
        codename='change_doctor',
        content_type=content_type_doctor,
    )

    delete_doctor = Permission.objects.get(
        codename='delete_doctor',
        content_type=content_type_doctor,
    )

    medical_staff_group.permissions.add(add_doctor, view_doctor, change_doctor, delete_doctor)
    user_group.permissions.add(view_doctor)

    return user_group, medical_staff_group


def create_users_for_tests(user_group, medical_staff_group) -> tuple:
    """Создает пользователей и добавляет им группы, функция принимает 2 группы.
     Возвращает: user, other_user, medical_staff, other_medical_staff"""
    user = User.objects.create(
        email='user@test.ru',
        fullname='Фамилия Имя Отчество',
        phone_number='+77777777771',
        password='test'
    )
    user_group.user_set.add(user)
    user.save()

    other_user = User.objects.create(
        email='other_user@test.ru',
        fullname='Фамилия Имя Отчество',
        phone_number='+77777777772',
        password='test'
    )
    user_group.user_set.add(other_user)
    other_user.save()

    medical_staff = User.objects.create(
        email='medical_staff@test.ru',
        fullname='Фамилия Имя Отчество',
        phone_number='+77777777773',
        password='test'
    )
    medical_staff_group.user_set.add(medical_staff)
    medical_staff.save()

    other_medical_staff = User.objects.create(
        email='other_medical_staff@test.ru',
        fullname='Фамилия Имя Отчество',
        phone_number='+77777777774',
        password='test'
    )
    medical_staff_group.user_set.add(other_medical_staff)
    other_medical_staff.save()

    return user, other_user, medical_staff, other_medical_staff
