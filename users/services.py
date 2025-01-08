import secrets

from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from services.models import Analysis, UsersAppointment
from users.models import User, History, Cart


def send_email_verification(self, user):
    """Присваивает пользователю токен и отправляет письмо со ссылкой на завершение регистрации."""
    token = secrets.token_hex(16)
    user.token = token

    user.save()

    host = self.request.get_host()
    link = f"http://{host}/users/email-confirm/{token}/"
    msg = (f'Здравствуйте, для подтверждения почты и регистрации на сайте перейдите по ссылке ниже.\n'
           f'{link}\n'
           f'Если вы не регистрировались на сайте, не переходите по ссылке.')

    send_mail(
        subject='Подтверждение почты для регистрации на сайте медицинской диагностики',
        message=msg,
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
    )


def convert_analysis_to_history(user: User, analysis: Analysis):
    """Создает объект модели History и записывает в него информацию из объекта Analysis."""

    message = (f"Наименование: {analysis.title}\n"
               f"Врач: {analysis.doctor}\n"
               f"Описание: {analysis.description}")

    History.objects.create(
        owner=user,
        service_info=message,
        price=analysis.price
    )


def convert_users_appointment_to_history(user: User, users_appointment: UsersAppointment):
    """Создает объект модели History и записывает в него информацию из объекта UsersAppointment."""

    service = users_appointment.get_service()

    message = (f"Наименование: {users_appointment.title}\n"
               f"Врач: {users_appointment.doctor}\n"
               f"Услуги на приеме: {service.title}\n"
               f"{service.description}")

    History.objects.create(
        owner=user,
        service_info=message,
        price=service.price
    )


def convert_to_history(request):
    """Переводит содержимое корзин в историю."""

    user = request.user
    cart_list = Cart.objects.filter(owner=user)

    for cart in cart_list:
        if cart.analysis:
            convert_analysis_to_history(user, cart.analysis)
            cart.delete()
        else:
            convert_users_appointment_to_history(user, cart.users_appointment)
            cart.delete()
