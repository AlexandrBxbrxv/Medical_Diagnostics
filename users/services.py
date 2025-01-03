import secrets

from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from services.models import Analysis, Appointment
from users.models import User, History


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
