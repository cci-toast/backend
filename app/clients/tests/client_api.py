import json

from rest_framework import status
from rest_framework.test import APITestCase


class ClientAPITest(APITestCase):
    def setUp(self):
        self.expected_clients = []

        # create first client
        response = self.client.generic('POST', '/api/clients', json.dumps({
            'first_name': 'Bruce',
            'last_name': 'Wayne',
            'birth_year': '1992',
            'email': 'bwayne@drexel.edu',
            'personal_annual_net_income': 10000.0,
            'additional_income': 5000.0,
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
            'advisor': None
        })

        # create second client
        response = self.client.generic('POST', '/api/clients', json.dumps({
            'first_name': 'Dick',
            'last_name': 'Grayson',
            'birth_year': '2000',
            'email': 'dgrayson@gmail.com',
            'personal_annual_net_income': 20000.0,
            'additional_income': 1000.0,
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
            'advisor': None
        })

    def test_post(self):
        response = self.client.generic('POST', '/api/clients', json.dumps({
            'first_name': 'Bao',
            'last_name': 'Batman',
            'birth_year': '1996',
            'email': 'jf91@drexel.edu',
            'personal_annual_net_income': 80000.0,
            'additional_income': 5000.0,
        }), content_type='application/json')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
            'advisor': None
        })

    def test_post_required(self):
        response = self.client.generic(
            'POST', '/api/clients', json.dumps({}), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'first_name': ['This field is required.'],
            'last_name': ['This field is required.'],
            'email': ['This field is required.'],
        })

    def test_get_list(self):
        # get the all list of clients
        response = self.client.generic('GET', '/api/clients')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_clients)

    def test_get_list_by_first_name(self):
        # filter clients by first_name
        response = self.client.generic('GET', '/api/clients', json.dumps({
            'first_name': 'Dick'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, [self.expected_clients[1]])

    def test_get_list_by_city(self):
        # filter clients by city
        response = self.client.generic('GET', '/api/clients', json.dumps({
            'city': 'Philadelphia'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_clients)

    def test_get_list_by_first_name_and_last_name(self):
        # filter clients by last_name and first_name
        response = self.client.generic('GET', '/api/clients', json.dumps({
            'first_name': 'Dick',
            'last_name': 'Wayne'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, [])

    def test_get_detail_with_valid_id(self):
        # get the client detail with valid id
        response = self.client.generic('GET', '/api/clients', json.dumps({
            'id': self.first_client_id
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_clients[0])

    def test_get_detail_with_non_exist_id(self):
        # get non-exist client
        response = self.client.generic('GET', '/api/clients', json.dumps({
            'id': '123e4567-e89b-12d3-a456-426655440000'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Object not exists.']
        })

    def test_get_detail_with_invalid_id(self):
        # get client detail with invalid id
        response = self.client.generic('GET', '/api/clients', json.dumps({
            'id': '1233-1222-122222'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Must be a valid UUID.']
        })

    def test_patch_with_valid_id(self):
        # change the client detail with valid id
        response = self.client.generic('PATCH', '/api/clients', json.dumps({
            'id': self.first_client_id,
            'first_name': 'Superman',
            'last_name': 'Bigboy'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_change = self.expected_clients[0].copy()
        expected_change['first_name'] = 'Superman'
        expected_change['last_name'] = 'Bigboy'
        self.assertEqual(response_data, expected_change)

    def test_patch_with_non_exist_id(self):
        # change the client detail with non-exist id
        response = self.client.generic('PATCH', '/api/clients', json.dumps({
            'id': '123e4567-e89b-12d3-a456-426655440000',
            'first_name': 'Superman',
            'last_name': 'Bigboy'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Object not exists.']
        })

    def test_patch_with_invalid_id(self):
        # change the client detail with invalid id
        response = self.client.generic('PATCH', '/api/clients', json.dumps({
            'id': '12ssfsdfsdfqweqdnqwkd',
            'first_name': 'Superman',
            'last_name': 'Bigboy'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Must be a valid UUID.']
        })

    def test_delete_with_valid_id(self):
        # change the client detail with valid id
        response = self.client.generic('DELETE', '/api/clients', json.dumps({
            'id': self.first_client_id,
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_change = self.expected_clients[0]
        expected_change['id'] = None
        self.assertEqual(response_data, expected_change)

        # make sure we only have one client left
        response = self.client.generic('GET', '/api/clients')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, [self.expected_clients[1]])

    def test_delete_with_non_exist_id(self):
        # change the client detail with non-exist id
        response = self.client.generic('DELETE', '/api/clients', json.dumps({
            'id': '123e4567-e89b-12d3-a456-426655440000',
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Object not exists.']
        })

    def test_delete_with_invalid_id(self):
        # change the client detail with invalid id
        response = self.client.generic('DELETE', '/api/clients', json.dumps({
            'id': '12ssfsdfsdfqweqdnqwkd',
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Must be a valid UUID.']
        })
