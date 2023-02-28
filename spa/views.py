from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth.mixins import UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import BasePermission

from spa.forms import SigninForm, SignupForm
from spa.forms import StyleFormMixin
from spa.models import CustomUser, Course, Lesson, Payment, UserSubscription
from rest_framework import viewsets, generics

from spa.serializer import LessonSerializer, CourseSerializer, PaymentSerializer, CustomUserSerializer, \
    CustomUserPaySerializer, UserSubscriptionSerializer


class SigninView(LoginView):
    template_name = 'spa/login.html'
    form_class = SigninForm


class SignupView(CreateView):
    template_name = 'spa/register.html'
    form_class = SignupForm
    success_url = reverse_lazy('spa:home')


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
class RulesCreateCourse(permissions.BasePermission):##UserPassesTestMixin
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
    permission_classes = (RulesCreateCourse,)##RulesPermissionsChangeCourse, RulesPermissionsDeleteCourse,
    permission_required = "spa.change_course"
class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    success_url = reverse_lazy('spa:Lesson_create')

class RulesCreateLesson(permissions.BasePermission):##UserPassesTestMixin
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
    permission_classes = (RulesPermissionsChangeLesson, )##SuperUserPermissionsObj

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

class PayListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
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

class PayRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):##permissions.BasePermission,UserPassesTestMixin
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    # permission_classes = (RulesPermissionsChangePayment, RulesPermissionsDeletePayment)##Snachala proverim funkciu, potom rascommetiruem

    permission_classes = (UserPermissionsObj, RulesPermissionsChangePayment, RulesPermissionsDeletePayment)##Zdes nakladivautsya permissions pohozhe
class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class PayCustomUserDetailAPIView(RetrieveAPIView):
    serializer_class = CustomUserPaySerializer
    queryset = CustomUser.objects.all()

class UserSubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = UserSubscriptionSerializer
    queryset = UserSubscription.objects.all()
    # template_name = 'spa/home.html'
    # success_url = reverse_lazy('spa:Course_create')
