import datetime
import json

from celery.schedules import schedule
from django.core.management import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):
    def handle(self, *args, **options):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS,
        )

        PeriodicTask.objects.create(

        interval=schedule,                  # we created this above.
        name='Importing contacts',          # simply describes this periodic task.
        task='proj.tasks.import_contacts',  # name of task.
        args=json.dumps(['arg1', 'arg2']),

        kwargs=json.dumps({

           'be_careful': True,

        }),

    expires=datetime.utcnow() + datetime.timedelta(seconds=30)

)