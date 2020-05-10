from rest_framework import status
import json

from rest_framework.test import APITestCase


class AuthAPITest(APITestCase):

    def setUp(self):
        pass

    def test_get_auth_token(self):
        response = self.client.post('/auth/registration', data={
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
