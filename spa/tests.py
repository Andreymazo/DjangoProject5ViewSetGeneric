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
    def setUp(self) -> None:
        self.user = CustomUser(
            email='test@12.ru',
        )
        self.user.set_password('qwert123asd')
        self.user.save()
        response = self.client.post(
            "/api/token/",
            {'email': 'test@12.ru', 'password': 'qwert123asd', 'is_active': 'True'},##, 'id': 4, 'is_superuser': False, 'is_staff': False
            # content_type="application/json"
        )

        self.access_token = response.json().get('access')
        print(response.json().get('access'))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    # client = APIClient()
    # client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    # response = client.get('/api/vehicles/')
    def test_create(self):
        response = self.client.post(
            "/home/UserSubscription/",
            {"profile_id": 4}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    # def test_get_profile(self):
    #     self.test_create()  # Chtobi ne nabivat zanovo setup
    #     response = self.client.get(
    #         f"/home/Profile/2",
    #     )
    #     self.assertEqual(
    #         response.status_code,
    #         status.HTTP_200_OK
    #     )
    #     self.assertEqual(
    #         response.json(),
    #         {
    #             "user": 3,
    #             "slug": "",
    #             "following_subscription": [1],
    #             "following_payment": [1],
    #             'subscription_info': [{'period': '18:06:12.271069',
    #                                    'status': True,
    #                                    'subscribed_on': '2023-03-01T18:06:12.271052+03:00'}]
    #
    #         }
    #     )
# def setUp(self):
#     self.username = 'admin'
#     self.password = 'admin'
#     self.datetime = 'Tue, 15 Nov 1994 08:12:31 GMT'
#     self.temperature = '15.6'
#     self.presence = '56'
#
#
# def test_presence_post(self):
#     #frame = 'presence=' + self.presence + '&datetime=2014-12-12 16:45:45'
#
#     c = Client()
#     c.login(username=self.username, password=self.password)
#     response = c.post('/datapresence', {'presence=' + self.presence + '&datetime=2014-12-12 16:45:45'},
#         content_type="application/x-www-form-urlencoded", HTTP_DATE=datetime)
#     self.assertEqual(response.status_code, 201)