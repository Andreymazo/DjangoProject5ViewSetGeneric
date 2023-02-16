from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from spa.forms import SigninForm, SignupForm
from spa.forms import StyleFormMixin
from spa.models import User, Course
from rest_framework import viewsets, generics

from spa.serializer import LessonSerializer, CourseSerializer


class SigninView(LoginView):
    template_name = 'spa/login.html'
    form_class = SigninForm

class SignupView(CreateView):
    template_name = 'spa/register.html'
    form_class = SignupForm
    success_url = reverse_lazy('spa:home')

class CourseListView(ListView):
    model = Course
    template_name = 'spa/home'
    success_url=reverse_lazy('spa:home')###home pomenyem potom
class CourseViewset(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer

class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class=CourseSerializer





