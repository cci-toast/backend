import json
from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class ClientAPITest(APITestCase):

    def setUp(self):
        self.expected_clients = []

        response = self.client.post('/auth/registration', data={
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.headers = response_data['key']
        # create first client

        response = self.client.post('/api/clients', data={
            'first_name': 'Bruce',
            'last_name': 'Wayne',
            'birth_year': '1992',
            'email': 'bwayne@drexel.edu',
            'personal_annual_net_income': 10000.0,
            'additional_income': 5000.0,
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.first_client_id = response_data['id']

        # expected data return by first client
        self.expected_clients.append({
            'id': self.first_client_id,
            'first_name': 'Bruce',
            'middle_name': '',
            'last_name': 'Wayne',
            'birth_year': 1992,
            'city': 'Philadelphia',
            'state': 'PA',
            'email': 'bwayne@drexel.edu',
            'personal_annual_net_income': '10000.00',
            'additional_income': '5000.00',
            'advisor': None,
            'current_year': date.today().year,
            'age': date.today().year - 1992,
            'total_annual_income': '15000.00',
            'household_annual_net_income': '15000.00'
        })

        # create second client
        response = self.client.post('/api/clients', data={
            'first_name': 'Dick',
            'last_name': 'Grayson',
            'birth_year': '2000',
            'email': 'dgrayson@gmail.com',
            'personal_annual_net_income': 20000.0,
            'additional_income': 1000.0,
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.second_client_id = response_data['id']

        # expected data return by second client
        self.expected_clients.append({
            'id': self.second_client_id,
            'first_name': 'Dick',
            'middle_name': '',
            'last_name': 'Grayson',
            'birth_year': 2000,
            'city': 'Philadelphia',
            'state': 'PA',
            'email': 'dgrayson@gmail.com',
            'personal_annual_net_income': '20000.00',
            'additional_income': '1000.00',
            'advisor': None,
            'current_year': date.today().year,
            'age': date.today().year - 2000,
            'total_annual_income': '21000.00',
            'household_annual_net_income': '21000.00',
        })
        # self.client.credentials()

    def test_post(self):
        response = self.client.post('/api/clients', data={
            'first_name': 'Bao',
            'last_name': 'Batman',
            'birth_year': '1996',
            'email': 'jf91@drexel.edu',
            'personal_annual_net_income': 80000.0,
            'additional_income': 5000.0,
        }, headers=self.headers)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data, {
            'id': response_data['id'],
            'first_name': 'Bao',
            'middle_name': '',
            'last_name': 'Batman',
            'birth_year': 1996,
            'city': 'Philadelphia',
            'state': 'PA',
            'email': 'jf91@drexel.edu',
            'personal_annual_net_income': '80000.00',
            'additional_income': '5000.00',
            'advisor': None,
            'current_year': date.today().year,
            'age': date.today().year - 1996,
            'total_annual_income': '85000.00',
            'household_annual_net_income': '85000.00'
        })
        # self.client.credentials()

    def test_post_required(self):
        response = self.client.post('/api/clients', data={})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'first_name': ['This field is required.'],
            'last_name': ['This field is required.'],
            'email': ['This field is required.'],
        })
        # self.client.credentials()

    def test_get_list(self):
        # get the all list of clients
        response = self.client.get('/api/clients')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'count': len(self.expected_clients),
            'next': None,
            'previous': None,
            'results': self.expected_clients
        })

    def test_get_list_by_first_name(self):
        # filter clients by first_name
        response = self.client.get('/api/clients', data={
            'first_name': 'Dick'
        })
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [self.expected_clients[1]]
        })

    def test_get_list_by_city(self):
        # filter clients by city
        response = self.client.get('/api/clients', data={
            'city': 'Philadelphia'
        })
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'count': len(self.expected_clients),
            'next': None,
            'previous': None,
            'results': self.expected_clients
        })

    def test_get_list_by_first_name_and_last_name(self):
        # filter clients by last_name and first_name
        response = self.client.get('/api/clients', data={
            'first_name': 'Dick',
            'last_name': 'Wayne'
        })
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        })

    def test_get_detail_with_valid_id(self):
        # get the client detail with valid id
        response = self.client.get('/api/clients/' + self.first_client_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_clients[0])

    def test_get_detail_with_non_exist_id(self):
        # get non-exist client
        response = self.client.get(
            '/api/clients/' + '123e4567-e89b-12d3-a456-426655440000')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_detail_with_invalid_id(self):
        # get client detail with invalid id
        response = self.client.get('/api/clients/' + '1233-1222-122222')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_with_valid_id(self):
        # change the client detail with valid id
        response = self.client.patch('/api/clients/' + self.first_client_id, data={
            'first_name': 'Superman',
            'last_name': 'Bigboy'
        })
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_change = self.expected_clients[0].copy()
        expected_change['first_name'] = 'Superman'
        expected_change['last_name'] = 'Bigboy'
        self.assertEqual(response_data, expected_change)

    def test_patch_with_non_exist_id(self):
        # change the client detail with non-exist id
        response = self.client.patch('/api/clients/123e4567-e89b-12d3-a456-426655440000', data={
            'first_name': 'Superman',
            'last_name': 'Bigboy'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_with_invalid_id(self):
        # change the client detail with invalid id
        response = self.client.patch('/api/clients/12ssfsdfsdfqweqdnqwkd', data={
            'first_name': 'Superman',
            'last_name': 'Bigboy'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_valid_id(self):
        # change the client detail with valid id
        response = self.client.delete('/api/clients/' + self.first_client_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # make sure we only have one client left
        response = self.client.get('/api/clients')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [self.expected_clients[1]]
        })

    def test_delete_with_non_exist_id(self):
        response = self.client.delete(
            '/api/clients/123e4567-e89b-12d3-a456-426655440000')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_invalid_id(self):
        response = self.client.delete('/api/clients/12ssfsdfsdfqweqdnqwkd')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
