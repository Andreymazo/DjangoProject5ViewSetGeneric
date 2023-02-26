from django.core.management import BaseCommand

from spa.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = CustomUser.objects.create(
            email= 'test@test.ru',
            is_superuser=True,
            is_staff=True
        )
        user.set_password('Lfirf111@')
        user.save()