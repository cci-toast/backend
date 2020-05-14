from rest_framework import status
import json

from rest_framework.test import APITestCase


class AuthAPITest(APITestCase):

    def setUp(self):
        #create a user to test login
        response = self.client.post('/auth/registration', data={
            'username': 'mario',
            'email': 'mario@email.com',
            'password1': 'mariopassword',
            'password2': 'mariopassword'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.post('/auth/logout/')

    def test_register_new_user(self):
        response = self.client.post('/auth/registration', data={
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': 'testpassword',
            'password2': 'testpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.post('/auth/logout/')

    def test_login_existing_user_with_valid_credentials(self):
        response = self.client.post('/auth/login/', data={
            'username': 'mario',
            'email': 'mario@email.com',
            'password': 'mariopassword'
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.post('/auth/logout/')

    def test_login_existing_user_with_invalid_credentials(self):
        response = self.client.post('/auth/login/', data={
            'username': 'dragon',
            'password': 'dragonpassword',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_register_required_info(self):
        response = self.client.post('/auth/registration', data={
            'username': 'patrick',
            'email': 'patrick@email.com',
            'password1': 'patrickpassword',
        })
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'password2': ['This field is required.']
        })

    def test_register_not_required_info(self):
        response = self.client.post('/auth/registration', data={
            'username': 'karen',
            'password1': 'karenpassword',
            'password2': 'karenpassword'
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.post('/auth/logout/')

    def test_register_with_non_matching_passwords(self):
        response = self.client.post('/auth/registration', data={
            'username': 'susan',
            'email': 'susan@email.com',
            'password1': 'susanpassword',
            'password2': 'karenpassword'
        })
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'non_field_errors': ["The two password fields didn't match."]
            })


    def test_get_clients_without_auth(self):
        self.client.post('/auth/logout/')
        response = self.client.get('/api/clients')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
