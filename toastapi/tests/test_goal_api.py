import json

from rest_framework import status
from rest_framework.test import APITestCase


class GoalAPITest(APITestCase):
    def setUp(self):
        self.expected_goals = []
        response = self.client.post('/auth/registration', data={
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.headers = response_data['key']

        # create client
        response = self.client.post('/api/clients', data={
            'first_name': 'David',
            'last_name': 'Rose',
            'birth_year': '1990',
            'email': 'alexis.schitt@gmail.com',
            'personal_annual_net_income': 100000.0,
            'additional_income': 5000.0
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.first_client_id = response_data['id']

        # create first goal
        response = self.client.post('/api/goals', data={
            'client': self.first_client_id,
            'goal_type': 'New car',
            'goal_value': 32000.0,
            'goal_end_date': '2025-01-01'
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.first_goal_id = response_data['id']

        self.expected_goals.append({
            'id': self.first_goal_id,
            'goal_type': 'New car',
            'goal_value': '32000.00',
            'goal_end_date': '2025-01-01'
        })

        # create second goal
        response = self.client.post('/api/goals', data={
            'client': self.first_client_id,
            'goal_type': 'New bag',
            'goal_value': 3200.0,
            'goal_end_date': '2021-02-12'
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.second_goal_id = response_data['id']

        self.expected_goals.append({
            'id': self.second_goal_id,
            'goal_type': 'New bag',
            'goal_value': '3200.00',
            'goal_end_date': '2021-02-12'
        })

    def test_post(self):
        response = self.client.post('/api/goals', data={
            'client': self.first_client_id,
            'goal_type': 'New bag',
            'goal_value': 3200.00,
            'goal_end_date': '2021-02-12'
        }, headers=self.headers)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data, {
            'id': response_data['id'],
            'goal_type': 'New bag',
            'goal_value': '3200.00',
            'goal_end_date': '2021-02-12'
        })

    def test_post_required(self):
        response = self.client.post('/api/goals', data={})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'goal_type': ['This field is required.'],
            'client': ['This field is required.']
        })

    def test_get_list_of_goals(self):
        # get all partners for a client
        response = self.client.get('/api/goals', headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'count': 2,
            'next': None,
            'previous': None,
            'results': self.expected_goals
        })

    def test_get_goal(self):
        response = self.client.get(
            '/api/goals/' + self.expected_goals[1]['id'], headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_goals[1])

    def test_get_goal_with_valid_id(self):
        # get partner item by id
        response = self.client.get(
            '/api/goals/' + self.first_goal_id, headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_goals[0])

    def test_get_goal_with_non_exist_id(self):
        # get non-existent partner
        response = self.client.get(
            '/api/goals/123e4567-e89b-12d3-a456-426655440000', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_goal_with_invalid_id(self):
        # get partner with invalid id
        response = self.client.get('/api/goals/50392', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_goal_with_valid_id(self):
        # patch a goal by id
        response = self.client.patch('/api/goals/' + self.first_goal_id, data={
            'goal_type': 'New Toyota Prius'
        }, headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_change = self.expected_goals[0].copy()
        expected_change['goal_type'] = 'New Toyota Prius'
        self.assertEqual(response_data, expected_change)

    def test_patch_goal_with_non_exist_id(self):
        # patch non-existent goal
        response = self.client.patch('/api/goals/123e4567-e89b-12d3-a456-426655440000', data={
            'goal_type': 'New Toyota Prius'
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_goal_with_invalid_id(self):
        # patch partner with invalid id
        response = self.client.patch('/api/goals/12345', data={
            'goal_type': 'New Toyota Prius'
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_goal_with_valid_id(self):
        # delete partner with id
        response = self.client.delete(
            '/api/goals/' + self.first_goal_id, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # make sure we have only one goal now
        response = self.client.get(
            '/api/goals?client=' + self.first_client_id, headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [self.expected_goals[1]]
        })

    def test_delete_with_non_exist_id(self):
        # delete non-existent goal
        response = self.client.delete(
            '/api/goals/123e4567-e89b-12d3-a456-426655440000', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_invalid_id(self):
        # delete non-existent goal
        response = self.client.delete('/api/goals/12345', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
