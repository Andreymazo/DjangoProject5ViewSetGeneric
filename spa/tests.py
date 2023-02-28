from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.test import APITestCase

class UserSubscriptionTestCase(APITestCase):
    def setUp(self)->None:
        self.user = User (
            username='test@test.ru',
        )
        self.user_set_password('qwert123asd')
        self.user.save()
        response = self.client.post(
            '/api/token/',
            {'username': 'test@test.ru', 'password': 'qwert123asd'}
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    def UserSubscription_create(self):
        response = self.client.post(
            'home/UserSubscription/',
        {"user": 1}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )



