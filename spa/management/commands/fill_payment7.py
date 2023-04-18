from datetime import datetime

from django.core.management import BaseCommand

from spa.models import CustomUser, Payment, Lesson, Profile


class Command(BaseCommand):
    def handle(self, *args, **options):
        payment_list = []
        # for user in CustomUser.objects.all():
        for user in Profile.objects.all():
            for i in range(2):
                payment_list.append(
                    Payment(
                        pro_filee=user,
                        date_of_payment=datetime.now(),
                        lesson=Lesson.objects.all().order_by('?').first(),
                        sum_of_payment=1000,
                        form_of_payment=Payment.PAYMENT_CARD
                    )
                )
        Payment.objects.bulk_create(payment_list)
