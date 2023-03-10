import requests
import json
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView
from drf_yasg.utils import swagger_auto_schema

from rest_framework.generics import UpdateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from spa.tasks import course_check
from config import settings
from spa.forms import SigninForm, SignupForm
from spa.forms import StyleFormMixin
from spa.models import CustomUser, Course, Lesson, Payment, UserSubscription, Profile, STATUS_START, STATUS_DONE
from rest_framework import viewsets, generics, status

from spa.serializer import LessonSerializer, CourseSerializer, PaymentSerializer, CustomUserSerializer, \
    CustomUserPaySerializer, UserSubscriptionSerializer, ProfileSerializer


class SigninView(LoginView):
    template_name = 'spa/login.html'
    form_class = SigninForm
    success_url = reverse_lazy('spa:home_course_view')


class SignupView(CreateView):
    template_name = 'spa/register.html'
    form_class = SignupForm
    success_url = reverse_lazy('spa:home_course_view')


# class CourseListView(ListView):
#     model = Course
#     # template_name = 'spa/course_list.html'
#     success_url=reverse_lazy('spa:Course_create')###home pomenyem potom
# class CourseCreateAPIView(generics.CreateAPIView):###Rabotaet home/ no nam lishnee, sozdaem na home/course_create/
#     serializer_class = CourseSerializer
#     queryset = Course.objects.all()##########################

from rest_framework import permissions


class RulesPermissionsChangeLesson(permissions.BasePermission):
    # def has_permission(self, request, view):
    #     if request.user.is_superuser:
    #         return True
    #     return False
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('spa.change_lesson', obj)


class RulesPermissionsDeleteLesson(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('spa.delete_lesson', obj)


class RulesPermissionsChangePayment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('spa.change_payment', obj)


class RulesPermissionsDeletePayment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('spa.delete_payment', obj)


class RulesPermissionsChangeCourse(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('spa.change_course', obj)


class RulesPermissionsDeleteCourse(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm('spa.delete_course', obj)


class RulesCreateCourse(permissions.BasePermission):  ##UserPassesTestMixin
    # def has_permission(self, request, view):
    #     # if request.user.is_superuser:
    #     #     return True
    #     # return False
    #
    #     return bool(request.user.is_superuser)

    # edit_methods = ("PUT", "PATCH")

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True

    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_superuser:
    #         return True
    #
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #     #
    #     # if obj.author == request.user:
    #     #     return True
    #     #
    #     # if request.user.is_staff and request.method not in self.edit_methods:
    #     #     return True
    #
    #     return False
    # def has_object_permission(self, request, view, obj):
    #     if request.method == 'POST' or "DELETE":
    #         if request.user.is_superuser:
    #             return True
    #         return False
    #     return obj.user == request.user
    # Read permissions are allowed to any request,
    # so we'll always allow GET, HEAD or OPTIONS requests.
    # if request.method in permissions.SAFE_METHODS:
    #     return True
    #
    # # Write permissions are only allowed to the owner of the snippet.
    # return obj.user == request.user.is_superuser

    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_superuser:
    #         return True
    #
    #     return obj == request.user


# class AuthorAllStaffAllButEditOrReadOnly(permissions.BasePermission):

# edit_methods = ("PUT", "PATCH")

# def has_permission(self, request, view):
#     if request.user.is_authenticated:
# return True

# def has_object_permission(self, request, view, obj):
#     if request.method == 'POST':
#         if request.user.is_superuser:
#             return True

# if request.method in permissions.SAFE_METHODS:
#     return True
#
# if obj.user == request.user:
#     return True
#
# if request.user.is_staff and request.method not in self.edit_methods:
#     return True

# return False
class CourseViewSet(viewsets.ModelViewSet, PermissionRequiredMixin):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    template_name = 'spa/home.html'
    success_url = reverse_lazy('spa:Course_create')
    # def get_serializer_class(self):##Esli request.user has_perms to odin serializer, esli net, to drugoi
    #     if self.request.user
    permission_classes = (RulesCreateCourse,)  ##RulesPermissionsChangeCourse, RulesPermissionsDeleteCourse,
    permission_required = "spa.change_course"


class CourseUpdateView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_update(self, serializer):####!!AttributeError: 'function' object has no attribute 'pk'
        self.object = serializer.save()
        # print("PPPPPPPPPPPP")
        course_check.delay(self.object.pk, self.object.pk)


    #
        # print(serializer)
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    success_url = reverse_lazy('spa:Lesson_create')


class RulesCreateLesson(permissions.BasePermission):  ##UserPassesTestMixin
    # def test_func(self):
    #     return self.request.user.is_superuser
    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_superuser:
    #         return True
    #     return False

    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_superuser:
    #         return True
    #
    #     return obj == request.user

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        else:
            return False


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (RulesCreateLesson,)

    ##Sozdavat mozhet novie tolko superuser (kak mozhno sozdavat owneru, esli ego ese net?)


# class SuperUserPermissionsObj(permissions.BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         if request.user.is_superuser:
#             return True
#
#         return obj == request.user
class LessonUpdateView(UpdateAPIView, UserPassesTestMixin, PermissionRequiredMixin):  ## ,
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (RulesPermissionsChangeLesson,)  ##SuperUserPermissionsObj

    # def test_func(self):
    #     self.object = self.get_object()
    #     return self.request.user == self.object.owner  ### Update mozhet delat owner, no poka u nas net sviazi s CustoUser, net owner
    # permission_required = "spa.change_lesson"## ishet po etomu url pochemuto: http://localhost:8000/users/?next=/home/lesson_list/1


# class LessonRetrieveView(RetrieveAPIView):
#     serializer_class = LessonSerializer
#     queryset = Lesson.objects.all()

class LessonRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (RulesPermissionsChangeLesson, RulesPermissionsDeleteLesson)


class PayListAPIView(generics.ListAPIView):##Vistavlennie scheta
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()



# import hashlib
#
# hash_object = hashlib.sha256(b'Hello World')
# hex_dig = hash_object.hexdigest()
#
# print(hex_dig)

class PayListCheckAPIView(generics.ListAPIView):#Proveryaem chto oplacheno po pk
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get(self, pk, *args, **kwargs):
        order = 1
        # lesson_pk = self.kwargs.get('pk')
        lesson_pk = self.kwargs.get('pk')
        lesson_1 = Lesson.objects.get(pk=3)  ###pk=1 oplachen, pk=2 poka ne oplachen (vozvrashaet raznie statusi
        payment=Payment.objects.get(pk=lesson_pk)
        # print('test ', lesson)
        print('test 1st  ', lesson_1)
        print('test 1st lesson_1.price lesson_1.name ', lesson_1.price, lesson_1.name)
        # lesson_item = Payment.objects.filter(pk=payment_pk).first()
        # print('test ', lesson_pk)
        # lesson_item = get_object_or_404(Lesson, pk=1)###constraint foreign pk (s tem zhe id)  uhodit oshibka no teper 404
        # p, created = Payment.objects.get_or_create(pk=2)
        # print('test 2nd ', lesson_item)
        # p = Lesson.objects.create(
        #     lesson=lesson_item
        # )
        p = lesson_1.id + order  ##Nomer zakaza priviazali k lesson_id
        order += 1
        print("Order number = ", p.payment)

        r = requests.post(
            "https://securepay.tinkoff.ru/v2/Init",

            json={
                "TerminalKey": settings.TERMINAL_KEY,
                "password": "9rgoqv88ygs8g7ed",
                "Name": f'{lesson_1.name}',
                "Price": f'{lesson_1.price}',
                "Quantity": 1.00,
                "Amount": 100000,

                "OrderId": p,

                "DATA": {
                    "Phone": "+71234567890",
                    "Email": "a@test.com"
                },
                "Receipt": {
                    "Email": "a@test.ru",
                    "Phone": "+79031234567",
                    "EmailCompany": "b@test.ru",
                    "Taxation": "osn",
                    "Items": [
                        {
                            "Name": f'{lesson_1.name}',
                            "Price": f'{lesson_1.price}',
                            "Quantity": 1.00,
                            "Amount": 100000,
                            "PaymentMethod": "full_prepayment",
                            "PaymentObject": "commodity",
                            "Tax": "vat10",
                            "Ean13": "0123456789"
                        },

                    ]
                }
            },
        )

        # lesson_item = get_object_or_404(Lesson, pk=lesson_pk)
        # p = Payment.objects.create(
        #             lesson=lesson_item

        # print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFf", Response({"Message": r.json().get("Message")}))
        # # Payment.objects.create(pro_filee_id=1, id=1, lesson_id=2, course_id=1,
        # #                        **r.json())  ##FK Error, poetomu zakommentil poka
        # # Payment.objects.create(**json)
        # print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFf", Response({"Message": r.json().get("Message")}))
        # for i in Response:

        # Payment.objects.create(id=2, lesson_id=1,course_id=1, Message=r.json().get("Message"))
        # Payment.objects.create(id=2, lesson_id=1,course_id=1, Success=r.json().get("Success"))
        # Payment.objects.create(id=2, lesson_id=1,course_id=1, Details=r.json().get("Details"))
        # Payment.objects.create(id=2, lesson_id=1,course_id=1, ErrorCode=r.json().get("ErrorCode"))
        # Payment.objects.create(id=2, lesson_id=1,course_id=1, PaymentURL=r.json().get("PaymentURL"))
        # Payment.objects.create(id=2, lesson_id=1,course_id=1, TerminalKey=r.json().get("TerminalKey"))
        # Payment.objects.create(id=2, lesson_id=1,course_id=1, Status=r.json().get("Status"))
        # Payment.objects.create(id=2, lesson_id=1,course_id=1, PaymentId=r.json().get("PaymentId"))
        # Payment.objects.create(id=2, lesson_id=1,course_id=1, OrderId=r.json().get("OrderId"))
        # Payment.objects.create(id=2, lesson_id=1,course_id=1, Amount=r.json().get("Amount"))
        return Response(
            {
                "Message": r.json().get("Message"),
                "Success": r.json().get("Success"),
                "Details": r.json().get("Details"),
                "ErrorCode": r.json().get("ErrorCode"),
                "PaymentURL": r.json().get("PaymentURL"),
                "TerminalKey": r.json().get("TerminalKey"),
                "Status": r.json().get("Status"),
                "PaymentId": r.json().get("PaymentId"),
                "OrderId": r.json().get("OrderId"),
                "Amount": r.json().get("Amount"),
                # "url": r.json()["PaymentURL"]
            }
        )



    # def get(self, pk, *args, **kwargs):
    # lesson_1 = Lesson.objects.get(pk=1)
    # r = requests.post(
    #     "https://securepay.tinkoff.ru/v2/Init",
    #
    #     json={
    #         "TerminalKey": settings.TERMINAL_KEY,
    #         "password": "9rgoqv88ygs8g7ed",
    #         "Name": f'{lesson_1.name}',
    #         "Price": f'{lesson_1.price}',
    #         "Quantity": 1.00,
    #         "Amount": 100000,
    #
    #         "OrderId": p,
    #
    #         "DATA": {
    #             "Phone": "+71234567890",
    #             "Email": "a@test.com"
    #         },
    #         "Receipt": {
    #             "Email": "a@test.ru",
    #             "Phone": "+79031234567",
    #             "EmailCompany": "b@test.ru",
    #             "Taxation": "osn",
    #             "Items": [
    #                 {
    #                     "Name": f'{lesson_1.name}',
    #                     "Price": f'{lesson_1.price}',
    #                     "Quantity": 1.00,
    #                     "Amount": 100000,
    #                     "PaymentMethod": "full_prepayment",
    #                     "PaymentObject": "commodity",
    #                     "Tax": "vat10",
    #                     "Ean13": "0123456789"
    #                 },
    #
    #             ]
    #         }
    #     },
    # )
    #
    # return Response(
    #         {
    #         "Message": r.json().get("Message"),
    #         "Success": r.json().get("Success"),
    #         "Details": r.json().get("Details"),
    #         "ErrorCode": r.json().get("ErrorCode"),
    #         "PaymentURL": r.json().get("PaymentURL")
    #         # "url": r.json()["PaymentURL"]
    #
    #         # ["PaymentURL"]
    #
    #         })


class UserPermissionsObj(permissions.BasePermission):

    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_superuser:
    #         return True
    #
    #     return obj == request.user

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True
        return False


class PayRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):  ##permissions.BasePermission,UserPassesTestMixin
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    # https://securepay.tinkoff.ru/v2/GetState

    # def post(self, request, *args, **kwargs):
    # def post(self, request, format=None):
    #     serializer = PaymentSerializer(data=request.data)
    #     print('test post', request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # lesson_pk = self.kwargs.get('pk')
    # lesson_item = Lesson.objects.filter(pk=lesson_pk).first()
    #
    # # p = Payment.objects.create(
    # #                 lesson=lesson_item
    # #
    # #             )
    # print("lesson_pk = ", lesson_pk, "lesson_item = ", lesson_item)#, "p = ", p
    #
    # data_for_request = {
    #     "TerminalKey": settings.TERMINAL_KEY,
    #     "Amount": lesson_item.price,
    #     "OrderId": "p.pk",
    #
    #     "DATA": {
    #         "Phone": "+71234567890",
    #         "Email": "a@test.com"
    #     },
    #     "Receipt": {
    #         "Email": "a@test.ru",
    #         "Phone": "+79031234567",
    #         "EmailCompany": "b@test.ru",
    #         "Taxation": "osn",
    #         "Items": [
    #             {
    #                 "Name": f'{Lesson.name}',
    #                 "Price": f'{Lesson.price}',
    #                 "Quantity": 1.00,
    #                 "Amount": 100000,
    #                 "PaymentMethod": "full_prepayment",
    #                 "PaymentObject": "commodity",
    #                 "Tax": "vat10",
    #                 "Ean13": "0123456789"
    #             },
    #
    #         ]
    #     }
    # }
    #

    # return super().request.post(request, *args, **kwargs)
    # permission_classes = (RulesPermissionsChangePayment, RulesPermissionsDeletePayment)##Snachala proverim funkciu, potom rascommetiruem

    # permission_classes = (UserPermissionsObj, RulesPermissionsChangePayment,
    #                       RulesPermissionsDeletePayment)  ##Zdes nakladivautsya permissions pohozhe
    # def post(self, *args, **kwargs):
    #         lesson_pk = self.kwargs.get('pk')
    #         # lesson_item = Lesson.objects.filter(pk=lesson_pk).first()##Ostalos s umoney
    #         lesson_item = get_object_or_404(Lesson, pk=lesson_pk)
    #         p = Payment.objects.create(
    #             lesson=lesson_item
    #
    #         )
    #     data_for_request = {
    #         "TerminalKey": settings.TERMINAL_KEY,
    #         "Amount": lesson_item.price,
    #         "OrderId": p.pk,
    #
    #         "DATA": {
    #             "Phone": "+71234567890",
    #             "Email": "a@test.com"
    #         },
    #         "Receipt": {
    #             "Email": "a@test.ru",
    #             "Phone": "+79031234567",
    #             "EmailCompany": "b@test.ru",
    #             "Taxation": "osn",
    #             "Items": [
    #                 {
    #                     "Name": f'{Lesson.name}',
    #                     "Price": f'{Lesson.price}',
    #                     "Quantity": 1.00,
    #                     "Amount": 100000,
    #                     "PaymentMethod": "full_prepayment",
    #                     "PaymentObject": "commodity",
    #                     "Tax": "vat10",
    #                     "Ean13": "0123456789"
    #                 },
    #
    #             ]
    #         }
    #     }
    #
    #         r = requests.post(
    #             'https://securepay.tinkoff.ru/v2/Init',
    #             data_for_request
    #
    #         )
    #         PaymentCheckLog.objects.create(**r.json())
    #         return Response(
    #             {
    #                 "url": r.json()['PaymentURL']
    #             }
    #         )


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class PayCustomUserDetailAPIView(RetrieveAPIView):
    serializer_class = CustomUserPaySerializer
    queryset = CustomUser.objects.all()


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubscriptionSerializer
    queryset = UserSubscription.objects.all()

class UserSubscriptionAPIView(APIView):## "course_subscribe": 1 Dobavlyaem/Udalyaem podpisku


    @swagger_auto_schema(responses={200: UserSubscriptionSerializer(many=True)})
    def post(self, *args, **kwargs):
        user = Profile.objects.get(user=self.request.user)
        # Попробуйте изменить эту деталь: (user_from=request.user) На
        # это: (user_from=User.objects.get(username=request.user)) Ваш
        # user_from должен быть экземпляром модели User, а не простым именем пользователя.
        course_id = self.request.data.get('course_subscribe')
        course_item = get_object_or_404(Course, pk=course_id)
        sub_item = UserSubscription.objects.filter(profile=user, course_subscribe=course_item)
        if sub_item.exists():
            sub_item.delete()
            message = "подписка удалена"
        else:
            UserSubscription.objects.create(profile=user, course_subscribe=course_item)
            message = "подписка добавлена"
        return Response({"message": message})




    # template_name = 'spa/home.html'
    # success_url = reverse_lazy('spa:Course_create')


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


    # class PaymentCheckView(View): ##Oplachivaem urok cherez UMoney
    #     def get(self, *args, **kwargs):
    #         lesson_pk = self.kwargs.get('pk')
    #         lesson_item = Lesson.objects.filter(pk=lesson_pk).first()
    #         context={
    #             # 'receiver': settings/YOOMONEY_WALLET,#Nado v settings vstavit svoi schet
    #             'label': f'{lesson_item.name}',
    #             'sum': f'{lesson_item.price}',
    #         }
    #         return render(self.request, 'spa/paymentform.html', context)


class PaymentCheckView(APIView):  ##Oplachivaem urok cherez Tinkoff
    pass
    # class PaymentCheckVieSet(viewsets.ModelViewSet):
    #         serializer_class = ProfileSerializer
    #         queryset = Payment.objects.all()

    # def post(self, request, *args, **kwargs):
    #     print('test post', self.some_data)
    #     return super().post(request, *args, **kwargs)
    # lesson_pk = self.kwargs.get('pk')
    # # lesson_item = Lesson.objects.filter(pk=lesson_pk).first()##Ostalos s umoney
    # lesson_item = get_object_or_404(Lesson, pk=lesson_pk)
    # p = PaymentCheck.objects.create(
    #     lesson=lesson_item
    # )
    # data_for_request = {
    #     "TerminalKey": settings.TERMINAL_KEY,
    #     "Amount": lesson_item.price,
    #     "OrderId": p.pk,
    #
    #     "DATA": {
    #         "Phone": "+71234567890",
    #         "Email": "a@test.com"
    #     },
    #     "Receipt": {
    #         "Email": "a@test.ru",
    #         "Phone": "+79031234567",
    #         "EmailCompany": "b@test.ru",
    #         "Taxation": "osn",
    #         "Items": [
    #             {
    #                 "Name": f'{Lesson.name}',
    #                 "Price": f'{Lesson.price}',
    #                 "Quantity": 1.00,
    #                 "Amount": 100000,
    #                 "PaymentMethod": "full_prepayment",
    #                 "PaymentObject": "commodity",
    #                 "Tax": "vat10",
    #                 "Ean13": "0123456789"
    #             },
    #
    #         ]
    #     }
    # }
    #
    # r = requests.post(
    #     'https://securepay.tinkoff.ru/v2/Init',
    #     data_for_request
    #
    # )
    # PaymentCheckLog.objects.create(**r.json())
    # return Response(
    #     {
    #         "url": r.json()['PaymentURL']
    #     }
    # )

    # context={
    #     # 'receiver': settings/YOOMONEY_WALLET,#Nado v settings vstavit svoi schet
    #     'label': f'{lesson_item.name}',
    #     'sum': f'{lesson_item.price}',
    # }
    # return render(self.request, 'spa/paymentform.html', context)
