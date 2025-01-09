import json

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    """Заполняет базу данных контентом."""
    help = "Заполняет базу данных из набора фикстур."

    def handle(self, *args, **kwargs):

        users_data_file = "fixtures/users_data.json"
        users_carts_file = "fixtures/users_carts.json"

        filtrated_users_data = []
        users_carts = []

        with open(users_data_file, mode='r', encoding='utf-8') as file:
            users_data = json.load(file)
            for item in users_data:
                if item["model"] == "users.cart":
                    users_carts.append(item)
                else:
                    filtrated_users_data.append(item)

        with open(users_carts_file, mode='w', encoding='utf-8') as file:
            json.dump(users_carts, file, indent=2, ensure_ascii=False)

        with open(users_data_file, mode='w', encoding='utf-8') as file:
            json.dump(filtrated_users_data, file, indent=2, ensure_ascii=False)

        fixtures = [
            "fixtures/auth_data.json",
            users_data_file,
            "fixtures/services_data.json",
            users_carts_file,
            "fixtures/main_data.json"
        ]

        for fixture in fixtures:
            self.stdout.write(self.style.NOTICE(f"Загружаю {fixture}..."))
            try:
                call_command("loaddata", fixture)
                self.stdout.write(self.style.SUCCESS(f"Успешно загружено: {fixture}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка при загрузке {fixture}: {e}"))
