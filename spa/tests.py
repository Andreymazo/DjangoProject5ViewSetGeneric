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
        self.user.set_password('qwert123asdf')
        self.user.save()
        response = self.client.post(
            "/api/token/",
            {'email': 'test@12.ru', 'password': 'qwert123asdf'},
            # content_type="application/json"
        )

        self.access_token = response.json().get('access')
        print(response.json().get('access'))
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
    def test_get_profile(self):
        self.test_create()#Chtobi ne nabivat zanovo setup
        response = self.client.get(
            f"/home/Profile/2",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                "user": 3,
                "slug": "",
                "following_subscription": [1],
                "following_payment": [1],
                'subscription_info': [{'period': '18:06:12.271069',
                                       'status': True,
                                       'subscribed_on': '2023-03-01T18:06:12.271052+03:00'}]

            }
        )



