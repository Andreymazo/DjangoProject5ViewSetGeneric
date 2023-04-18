from django.core.management import BaseCommand

from spa.models import UserSubscription, Profile, Course, Payment


class Command(BaseCommand):

    def handle(self, *args, **options):
        # subns = ['foreign_papa', 'Mike', 'Piter']##Sozdaem 3 profila na 3 userov
##############################################################
        usersubscription = UserSubscription.objects.create(
            profile_id=Profile.objects.get(pk=2).id,  ##Podpiski 2ogo profila
            course_subscribe=Course(pk=1),  ##Na pervii course
        )
        usersubscription.save()
        usersubscription = UserSubscription.objects.create(
            profile_id=Profile.objects.get(pk=1).id,  ##Podpiski 1ogo profila
            course_subscribe=Course(pk=1),  ##Na pervii course
        )
        # index+=1
        usersubscription.save()
        usersubscription = UserSubscription.objects.create(
            profile_id=Profile.objects.get(pk=2).id,  ##Podpiski 2ogo profila
            course_subscribe=Course(pk=2),  ##Na 2 course
        )

        usersubscription.save()
        usersubscription = UserSubscription.objects.create(
            profile_id=Profile.objects.get(pk=3).id,  ##Podpiski 3ogo profila
            course_subscribe=Course(pk=2),  ##Na 2 course
        )

        usersubscription.save()
########################################################### Nizhe proverki
        # a=Profile.objects.get(pk=1).id
        # print('FFFFFFFFFFFFFFFF', a)
        # a = UserSubscription.objects.all().get(pk=1) ##Vitaskivaem email usera
        # b = UserSubscription.objects.filter(pk=1).all()## Chto s etim, chto bez etogo --- .select_related("profile")
        # # # print(a.profile_id)
        # for i in b:
        #     print(i.profile.email)
        b = UserSubscription.objects.all().filter(course_subscribe_id=1)## pk - nomer podpiski, nam nado otsortirovat podpiski po nomeru coursa,  no na 1 course podpisano 2 profila, otsilaet tolko na odin##### Etonerabotaetinemeshaet#### .select_related("profile")
        # b = UserSubscription.objects.all().filter(pk=pk).profile.user.email ##Zdes mi nahodim email customuser Если раскомментировать и закомментировать 34 строчку, то отсылка будет на емэйлы кастомюзеров
        # # print(a.profile_id)
        for i in b:  ####Probegaemsya po emailam i obrabativaem oshibki po analogii kak v zakommenchennom nizhe
            print(f'Otsilaem na 1 email podpiski  obnovlennogo Course_________________ {i.profile.email}')##i.profile.user.email (esli hotim customuser slat emaili)
        filter_payments = {"Success": True}
        payment_list = Payment.objects.filter(**filter_payments)
        if payment_list.exists():
            for i in payment_list:
                print(f'otsilaem na email {i.pro_filee.email} profilya kotorie ne oplatili schet')

# import hashlib
# # text_string = text.text.encode('utf-8')
# hash_object = hashlib.sha256(b'140000Подарочная карта на 1400.00 рублей21050119rgoqv88ygs8g7ed1677659270153DEMO').encode('utf-8')
# hex_dig = hash_object.hexdigest()
#
# print(hex_dig)