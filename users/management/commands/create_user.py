from django.contrib.auth.models import Group
from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Создает пользователя."""
    def handle(self, *args, **options):
        email = input("Email: ")
        password = input("Пароль: ")

        user = User.objects.create(
            email=email
        )

        user.set_password(password)

        user_group = Group.objects.get(name='user')
        user_group.user_set.add(user)

        user.save()
