from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.urls import path, include

from config import settings
from spa.apps import SpaConfig
from spa.views import SigninView, SignupView, CourseViewSet, LessonListAPIView, LessonUpdateView, \
    LessonCreateAPIView, LessonRetrieveView, LessonRetrieveUpdateDestroy, PayListAPIView, \
    PayCustomUserDetailAPIView, PayRetrieveUpdateDestroyAPIView  # , CourseCreateAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
#CourseListView,
app_name = SpaConfig.name##Ne pokazal nam obyavlenia prilozhenia
router = DefaultRouter()
router.register(r'home', CourseViewSet.as_view({'get': 'list'}), basename='home')

urlpatterns = [
               path('', SigninView.as_view(template_name='spa/login.html'), name='login'),
               path('register', SignupView.as_view(template_name='spa/register.html'), name='register'),
               path('course_list/', CourseViewSet.as_view({'get': 'list'}), name='home_course_view'),#template_name='spa/home.html'
               # path('home/', CourseCreateAPIView.as_view(), name='home'),
               path('home/course_create/', CourseViewSet.as_view({ "post": "create"}), name='home'),#template_name='spa/course_list.html'###,"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"
               path('home/lesson_list/', LessonListAPIView.as_view(), name='lesson_list'),
               path('home/lesson_list/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
               path('home/lesson_list/<int:pk>', LessonUpdateView.as_view(), name='lesson_update'),
               path('home/lesson_list/<int:pk>', LessonRetrieveView.as_view(), name='lesson_update'),
               path('home/lesson_detail/<int:pk>', LessonRetrieveUpdateDestroy.as_view(), name='lesson_RetrieveUpdateDestroy'),
               path('pay_list/', PayListAPIView.as_view()),
               path('pay/<int:pk>', PayCustomUserDetailAPIView.as_view()),
               path('pay_update/<int:pk>', PayRetrieveUpdateDestroyAPIView.as_view()),
               path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
               path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
               ]
              # + router.urls
#
#     [
#     ,
#
#
# ]

