import json

from rest_framework import status
from rest_framework.test import APITestCase


class ChildrenAPITest(APITestCase):
    def setUp(self):
        self.expected_children = []

        # create client
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
        self.client_id = response_data['id']

        # create first children
        response = self.client.generic('POST', '/api/children', json.dumps({
            'client': self.client_id,
            'first_name': 'Dick',
            'birth_year': 2000,
            'planning_on_college': True,
            'in_college': False
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.expected_children.append(response_data)

        # create second children
        response = self.client.generic('POST', '/api/children', json.dumps({
            'client': self.client_id,
            'first_name': 'Alex',
            'birth_year': 2000,
            'planning_on_college': False,
            'in_college': False
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.expected_children.append(response_data)

    def test_post(self):
        self.assertEqual(self.expected_children[0], {
            'id': self.expected_children[0]['id'],
            'first_name': 'Dick',
            'birth_year': 2000,
            'planning_on_college': True,
            'in_college': False
        })

        self.assertEqual(self.expected_children[1], {
            'id': self.expected_children[1]['id'],
            'first_name': 'Alex',
            'birth_year': 2000,
            'planning_on_college': False,
            'in_college': False
        })

    def test_post_required(self):
        response = self.client.generic(
            'POST', '/api/children', json.dumps({}), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'client': ['This field is required.'],
            'first_name': ['This field is required.']
        })

    def test_get_detail(self):
        # get the detail of a children
        response = self.client.generic('GET', '/api/children', json.dumps({
            'client': self.client_id,
            'id': self.expected_children[0]['id']
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_children[0])

    def test_get_list(self):
        # get the all list of children
        response = self.client.generic('GET', '/api/children', json.dumps({
            'client': self.client_id
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_children)

    def test_get_required(self):
        response = self.client.generic('GET', '/api/children')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'client': ['This field is required.']
        })

    def test_patch(self):
        response = self.client.generic('PATCH', '/api/children', json.dumps({
            'client': self.client_id,
            'id': self.expected_children[0]['id'],
            'first_name': 'Bruce'
        }), content_type='application/json')

        modified_child = self.expected_children[0].copy()
        modified_child['first_name'] = 'Bruce'
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, modified_child)

    def test_patch_required(self):
        response = self.client.generic('PATCH', '/api/children', json.dumps({
            'first_name': 'Bruce'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'client': ['This field is required.'],
        })

        response = self.client.generic('PATCH', '/api/children', json.dumps({
            'client': self.client_id,
            'first_name': 'Bruce'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['This field is required.'],
        })

    def test_delete(self):
        # change the client detail with valid id
        response = self.client.generic('DELETE', '/api/children', json.dumps({
            'client': self.client_id,
            'id': self.expected_children[0]['id'],
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_change = self.expected_children[0]
        expected_change['id'] = None
        self.assertEqual(response_data, expected_change)

        # make sure we only have one client left
        response = self.client.generic('GET', '/api/children', json.dumps({
            'client': self.client_id
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, [self.expected_children[1]])