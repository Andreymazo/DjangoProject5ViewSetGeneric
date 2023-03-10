from django.core.management import BaseCommand

from spa.models import Course


class Command(BaseCommand):

    def handle(self, *args, **options):
       crss = ['Python', 'Astrology']

       for i in crss:
            course = Course.objects.create(
                name=i,
                description="Wondeful things"
            )
            course.save()
