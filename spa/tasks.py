from smtplib import SMTPRecipientsRefused, SMTPResponseException

from celery import shared_task
from django.core.mail import send_mail
from celery import shared_task

from config import settings
from spa.models import STATUS_START, UserSubscription, Course, Mailinglog, STATUS_DONE, Payment


@shared_task
def course_check(course_pk, pk):
    a = UserSubscription.objects.all().filter(pk=pk).first()
    # b = UserSubscription.objects.all()
    # for j in b:
    #     print('UserSubscription.objects.all().filter(pk=1)', j)
    # a.profile.email
    print(a.profile.user.email)
    # for i in a:
    #
    #     print('UserSubscription.objects.all().filter(pk=1).first().profile.user.email ===== ', i) #UserSubscription.status_send=== True 2023-03-09 04:16:01.754036+00:00 07:16:01.761341
    print('UserSubscription.status_send=== =', UserSubscription.objects.all().filter(pk=pk).first().status_send)

    if UserSubscription.objects.all().filter(pk=pk).first().status_send:  ##Esli eshe ne otoslano, to otsilaem
        #     # send_mail(subject=, message=,  recipient_list=,fail_silently=False, )
        # for i in Course.pro_file:
        print('____________________________________')
        # b = UserSubscription.objects.select_related("profile").all() # Zdes mi nahodim email profile
        b = UserSubscription.objects.all().filter(course_subscribe_id=pk)## pk - nomer course, no na 1 course podpisano 2 profila, otsilaet tolko na odin###select_related("profile").###
        # b = UserSubscription.objects.all().filter(pk=pk).profile.user.email ##Zdes mi nahodim email customuser Если раскомментировать и закомментировать 34 строчку, то отсылка будет на емэйлы кастомюзеров
        # # print(a.profile_id)
        for i in b:  ####Probegaemsya po emailam i obrabativaem oshibki po analogii kak v zakommenchennom nizhe
            print(f'Otsilaem na 1 email podpiski  obnovlennogo Course_________________ {i.profile.email}')##i.profile.user.email (esli hotim customuser slat emaili)
            try:
                res = send_mail(subject='test',
                                message='test',
                                from_email=settings.EMAIL_HOST_USER,
                                recipient_list=[i.profile.email],
                                fail_silently=False)
                if res:
                    Mailinglog.objects.create(
                        ####Zapisivaem pochtu, resultat otpravki i vremia samo zapisivaetsia#########
                        mailing=i,
                        result=res
                    )
            except ValueError as e:
                print(e)
                pass
            except SMTPResponseException as e:
                error_code = e.smtp_code
                error_message = e.smtp_error
                if error_code == 550:  # возможно, по-другому надо доставать, типа e.errno
                    print("Error code:" + f'{error_code}')
                    print("Message:" + f'{error_message}')
                    pass
            except SMTPRecipientsRefused as e:
                print(e)
                pass

    print(f"test course_pk Course.pro_file.name UserSubscription.status_send {course_pk} ")  # {Course.pro_file(pro_file_id=2)}==   print(f"test course_pk Course.pro_file.name UserSubscription.status_send {course_pk} {Course.pro_file(pro_file_id=2)}")#
    # TypeError: 'ForwardManyToOneDescriptor' object is not callable

    UserSubscription.objects.all().filter(pk=pk).first().status_send = STATUS_DONE##Posle rassilki opuskaem flag
@shared_task()
def filter_check():
    filter_payments = {"Success": True}
    payment_list = Payment.objects.filter(**filter_payments)
    print('_______________', Payment.objects.filter(pk=1).first())
    if payment_list.exists():
        for i in payment_list:
            # print(f'otsilaem na email {i.pro_filee.email} profilya kotorie ne oplatili schet')
            send_mail(
                subject='Oplata',
                message='oplatite oplatu',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[i.pro_filee.email],
                fail_silently=False)