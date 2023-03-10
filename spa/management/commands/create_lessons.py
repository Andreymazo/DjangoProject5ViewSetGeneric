from django.core.management import BaseCommand

from spa.models import Lesson, Course


class Command(BaseCommand):


    def handle(self, *args, **options):
        lessns_1Crs = ['1st Astrology lssn', '2 lesson for Astrology']##lssns for 1st Course
        for i in lessns_1Crs:
            lesson = Lesson.objects.create(
                name=i,
                smth=Course(pk=1),##Svyaz s course
                description="Wondeful things"
            )

            lesson.save()

            lessns_2Crs = ['1st Python lssn', '2nd Python lesson']  ##lssns for 2st Python

        for i in lessns_2Crs:
            lesson = Lesson.objects.create(
                    name=i,
                    smth=Course(pk=2),  ##Svyaz s course
                    description="Craceful things"
                )

            lesson.save()
