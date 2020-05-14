import json

from rest_framework import status
from rest_framework.test import APITestCase


class ActionItemAPITest(APITestCase):
    def setUp(self):
        self.expected_action_items = []
        #authenticate
        response = self.client.post('/auth/registration', data={
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.headers = response_data['key']

        # create a client
        response = self.client.post('/api/clients', data={
            'first_name': 'Kai',
            'last_name': 'Anderson',
            'birth_year': '1990',
            'email': 'kai.anderson@gmail.com',
            'personal_annual_net_income': 800000.0,
            'additional_income': 10000.0
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.first_client_id = response_data['id']

        # create first action item
        response = self.client.post('/api/action_items', data={
            'client': self.first_client_id,
            'description': 'Set aside $1,600 for emergency savings',
            'completed': False
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.first_action_item_id = response_data['id']

        self.expected_action_items.append({
            'id': self.first_action_item_id,
            'description': 'Set aside $1,600 for emergency savings',
            'completed': False
        })

        # create second action item
        response = self.client.post('/api/action_items', data={
            'client': self.first_client_id,
            'description': 'Set aside $500 to repay debt this month',
            'completed': True
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.second_action_item_id = response_data['id']

        self.expected_action_items.append({
            'id': self.second_action_item_id,
            'description': 'Set aside $500 to repay debt this month',
            'completed': True
        })

    def test_post(self):
        response = self.client.post('/api/action_items', data={
            'client': self.first_client_id,
            'description': 'Set aside $500 to repay debt this month',
            'completed': True
        }, headers=self.headers)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data, {
            'id': response_data['id'],
            'description': 'Set aside $500 to repay debt this month',
            'completed': True
        })

    def test_get_list_of_items(self):
        # get all action items for a client
        response = self.client.get('/api/action_items', headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'count': 2,
            'next': None,
            'previous': None,
            'results': self.expected_action_items
        })

    def test_get_single_action_item(self):
        # get the detail of a children
        response = self.client.get(
            '/api/action_items/' + self.expected_action_items[0]['id'], headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_action_items[0])

    def test_get_action_item_with_valid_id(self):
        # get action item by id
        response = self.client.get(
            '/api/action_items/' + self.first_action_item_id, headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_action_items[0])

    def test_get_action_item_with_non_exist_id(self):
        # get non-existent action item
        response = self.client.get(
            '/api/action_items/123e4567-e89b-12d3-a456-426655440000', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_action_item_with_invalid_id(self):
        # get actiion item with invalid id
        response = self.client.get('/api/action_items/50392', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_item_with_valid_id(self):
        # patch an action item by id
        response = self.client.patch('/api/action_items/' + self.first_action_item_id, data={
            'completed': True
        }, headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_change = self.expected_action_items[0].copy()
        expected_change['completed'] = True
        self.assertEqual(response_data, expected_change)

    def test_patch_item_with_non_exist_id(self):
        # patch non-exsitent item
        response = self.client.patch('/api/action_items/123e4567-e89b-12d3-a456-426655440000', data={
            'completed': True
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_item_with_invalid_id(self):
        # patch action item with invalid id
        response = self.client.patch('/api/action_items/12345', data={
            'completed': True
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item_with_valid_id(self):
        # delete action item with id
        response = self.client.delete(
            '/api/action_items/' + self.first_action_item_id, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # make sure we only have one action item left
        response = self.client.get(
            '/api/action_items?client=' + self.first_client_id, headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [self.expected_action_items[1]]
        })

    def test_delete_with_non_exist_id(self):
        # delete non-existent action item
        response = self.client.delete(
            '/api/action_items/123e4567-e89b-12d3-a456-426655440000', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_invalid_id(self):
        # delete non-existent action item
        response = self.client.delete('/api/action_items/12345', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
