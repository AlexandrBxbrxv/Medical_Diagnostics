from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    """Заполняет базу данных контентом."""
    help = "Заполняет базу данных из набора фикстур."

    def handle(self, *args, **kwargs):
        fixtures = [
            "fixtures/auth_data.json",
            "fixtures/users_data.json",
            "fixtures/main_data.json",
            "fixtures/services_data.json"
        ]

        for fixture in fixtures:
            self.stdout.write(self.style.NOTICE(f"Загружаю {fixture}..."))
            try:
                call_command("loaddata", fixture)
                self.stdout.write(self.style.SUCCESS(f"Успешно загружено: {fixture}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка при загрузке {fixture}: {e}"))
