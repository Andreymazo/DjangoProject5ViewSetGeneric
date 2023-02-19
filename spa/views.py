from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView

from spa.forms import SigninForm, SignupForm
from spa.forms import StyleFormMixin
from spa.models import User, Course, Lesson
from rest_framework import viewsets, generics

from spa.serializer import LessonSerializer, CourseSerializer

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
class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    template_name = 'spa/home.html'
    success_url = reverse_lazy('spa:Course_create')
class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    success_url = reverse_lazy('spa:Lesson_create')
class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class=CourseSerializer
    queryset = Lesson.objects.all()

class LessonUpdateView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

class LessonRetrieveView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
class LessonRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()




