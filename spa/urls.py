from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.urls import path

from config import settings
from spa.apps import SpaConfig
from spa.views import SigninView, SignupView, CourseViewset
app_name = SpaConfig.name##Ne pokazal nam obyavlenia prilozhenia
router = DefaultRouter()
router.register(r'home', CourseViewset, basename='home')

urlpatterns = [path('', SigninView.as_view(template_name='spa/login.html'), name='login'),
               path('register', SignupView.as_view(template_name='spa/register.html'), name='register'),
               path('home/', SignupView.as_view(template_name='spa/home.html'), name='home')
               ] + router.urls
#
#     [
#     ,
#
#
# ]

