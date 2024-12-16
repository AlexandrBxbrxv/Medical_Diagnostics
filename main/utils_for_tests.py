# Эти функции для импорта в setUp метод в тестах

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from services.models import Doctor, Appointment, Analysis
from users.models import User


def create_groups_for_test() -> tuple:
    """Создает и заполняет группы для тестов. Возвращает: user_group, medical_staff_group"""
    medical_staff_group = Group.objects.create(name='medical_staff')
    user_group = Group.objects.create(name='user')

    # permissions for Doctor ########################################
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

    # permissions for Appointment ###################################
    content_type_appointment = ContentType.objects.get_for_model(Appointment)

    add_appointment = Permission.objects.get(
        codename='add_appointment',
        content_type=content_type_appointment,
    )

    view_appointment = Permission.objects.get(
        codename='view_appointment',
        content_type=content_type_appointment,
    )

    change_appointment = Permission.objects.get(
        codename='change_appointment',
        content_type=content_type_appointment,
    )

    delete_appointment = Permission.objects.get(
        codename='delete_appointment',
        content_type=content_type_appointment,
    )

    # permissions for Analysis ######################################
    content_type_analysis = ContentType.objects.get_for_model(Analysis)

    add_analysis = Permission.objects.get(
        codename='add_analysis',
        content_type=content_type_analysis,
    )

    view_analysis = Permission.objects.get(
        codename='view_analysis',
        content_type=content_type_analysis,
    )

    change_analysis = Permission.objects.get(
        codename='change_analysis',
        content_type=content_type_analysis,
    )

    delete_analysis = Permission.objects.get(
        codename='delete_analysis',
        content_type=content_type_analysis,
    )

    medical_staff_group.permissions.add(add_doctor, view_doctor, change_doctor, delete_doctor)
    medical_staff_group.permissions.add(add_appointment, view_appointment, change_appointment, delete_appointment)
    medical_staff_group.permissions.add(add_analysis, view_analysis, change_analysis, delete_analysis)

    user_group.permissions.add(view_doctor, view_appointment, view_analysis)

    return user_group, medical_staff_group


def create_users_for_tests(user_group: Group, medical_staff_group: Group) -> tuple:
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


def create_doctors_for_tests(medical_staff: User, other_medical_staff: User) -> tuple:
    """Создает 2 объекта модели Doctor от разных пользователей. Возвращает: doctor, others_doctor"""
    doctor = Doctor.objects.create(
        owner=medical_staff,
        fullname='test',
        speciality='test',
        education='test',
        experience=1
    )

    others_doctor = Doctor.objects.create(
        owner=other_medical_staff,
        fullname='test',
        speciality='test',
        education='test',
        experience=1
    )

    return doctor, others_doctor


def create_appointments_for_tests(medical_staff: User, other_medical_staff: User) -> tuple:
    """Создает 2 объекта модели Appointment от разных пользователей. Возвращает: appointment, others_appointment"""
    appointment = Appointment.objects.create(
        owner=medical_staff,
        title='test',
        treatment_room=1
    )

    others_appointment = Appointment.objects.create(
        owner=other_medical_staff,
        title='test',
        treatment_room=1
    )

    return appointment, others_appointment


def create_analysis_for_tests(medical_staff: User, other_medical_staff: User) -> tuple:
    """Создает 2 объекта модели Analysis от разных пользователей. Возвращает: analysis, others_analysis"""
    analysis = Analysis.objects.create(
        owner=medical_staff,
        title='test',
        description='test',
        preparation='test',
        treatment_room=1,
        price=1
    )

    others_analysis = Analysis.objects.create(
        owner=other_medical_staff,
        title='test',
        description='test',
        preparation='test',
        treatment_room=1,
        price=1
    )

    return analysis, others_analysis
