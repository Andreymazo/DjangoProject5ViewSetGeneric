# from django.contrib.auth.models import User
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()
from rest_framework import status

from rest_framework.test import APITestCase

from config import settings


from spa.models import CustomUser
class UserSubscriptionTestCase(APITestCase):
    def setUp(self)->None:

        self.user = CustomUser(
            email='test@12.ru',
        )
        self.user.set_password('qwert123asd')
        self.user.save()
        response = self.client.post(
            '/api/token/',
            {'email': 'test@12.ru', 'password': 'qwert123asd'},
            content_type="application/json"
        )
        print(response.status_code)
        self.access_token = response.json().get('access')

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    def test_create(self):
        response = self.client.post(
            "/home/UserSubscription/",
        {"user": 6}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )



