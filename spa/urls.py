from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.urls import path, include

from config import settings
from spa.apps import SpaConfig
from spa.views import SigninView, SignupView, CourseViewSet,  LessonListAPIView, LessonUpdateView, \
    LessonCreateAPIView, LessonRetrieveView, LessonRetrieveUpdateDestroy
#CourseListView,
app_name = SpaConfig.name##Ne pokazal nam obyavlenia prilozhenia
router = DefaultRouter()
router.register(r'home', CourseViewSet.as_view({'get': 'list'}), basename='home')

urlpatterns = [
               path('', SigninView.as_view(template_name='spa/login.html'), name='login'),
               path('register', SignupView.as_view(template_name='spa/register.html'), name='register'),
               path('home/', CourseViewSet.as_view({'get': 'list'}), name='home'),#template_name='spa/home.html'
               path('home/course_create/', CourseViewSet.as_view({"get": "retrieve", "post": "create", "put": "update", "patch": "partial_update", "delete": "destroy"}), name='home'),#template_name='spa/course_list.html'
               path('home/lesson_list/', LessonListAPIView.as_view(), name='lesson_list'),
               path('home/lesson_list/create', LessonCreateAPIView.as_view(), name='lesson_create'),
               path('home/lesson_list/<int:pk>', LessonUpdateView.as_view(), name='lesson_update'),
               path('home/lesson_list/<int:pk>', LessonRetrieveView.as_view(), name='lesson_update'),
               path('home/lesson_list/<int:pk>', LessonRetrieveUpdateDestroy.as_view(), name='lesson_RetrieveUpdateDestroy'),
               ]
              # + router.urls
#
#     [
#     ,
#
#
# ]

