from datetime import datetime

from django.core.management import BaseCommand

from spa.models import CustomUser, Payment, Lesson


class Command(BaseCommand):
    def handle(self, *args, **options):
        payment_list = []
        for user in CustomUser.objects.all():
            for i in range(10):
                payment_list.append(
                    Payment(
                        user=user,
                        date_of_payment=datetime.now(),
                        lesson=Lesson.objects.all().order_by('?').first(),
                        sum_of_payment=1000,
                        form_of_payment=Payment.PAYMENT_CARD
                    )
                )
        Payment.objects.bulk_create(payment_list)
