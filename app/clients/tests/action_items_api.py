import json

from rest_framework import status
from rest_framework.test import APITestCase


class ActionItemAPITest(APITestCase):
    def setUp(self):
        self.expected_action_items = []
        #create a client 
        response = self.client.generic('POST', '/api/clients', json.dumps({
            'first_name': 'Kai',
            'last_name': 'Anderson',
            'birth_year': '1990',
            'email': 'kai.anderson@gmail.com',
            'personal_annual_net_income': 800000.0,
            'additional_income': 10000.0
            }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.first_client_id = response_data['id']

        #create first action item 
        response = self.client.generic('POST', '/api/action_items', json.dumps({
            'client': self.first_client_id,
            'description': 'Set aside $1,600 for emergency savings',
            'completed': False
            }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.first_action_item_id = response_data['id']
        
        self.expected_action_items.append({
            'id': self.first_action_item_id,
            'description': 'Set aside $1,600 for emergency savings',
            'completed': False
        })

        #create second action item
        response = self.client.generic('POST', '/api/action_items', json.dumps({
            'client': self.first_client_id,
            'description': 'Set aside $500 to repay debt this month',
            'completed': True
            }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.second_action_item_id = response_data['id']

        self.expected_action_items.append({
            'id': self.second_action_item_id,
            'description': 'Set aside $500 to repay debt this month',
            'completed': True
        })   



    def test_post(self):
        response = self.client.generic('POST', '/api/action_items', json.dumps({
            'client': self.first_client_id,
            'description': 'Set aside $500 to repay debt this month',
            'completed': True
            }), content_type='application/json')
        response_data = json.loads(response.content)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'id': response_data['id'],
            'description': 'Set aside $500 to repay debt this month',
            'completed': True
        })
    

    def test_get_list_of_items(self):
        #get all action items for a client
        response = self.client.generic('GET', '/api/action_items', json.dumps({
            'client': self.first_client_id
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_action_items)
    
    def test_get_action_item_with_valid_id(self):
        #get action item by id 
        response = self.client.generic('GET', '/api/action_items', json.dumps({
            'id': self.first_action_item_id,
            'client': self.first_client_id
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_action_items[0])       

    def test_get_action_item_with_non_exist_id(self):
        #get non-existent action item 
        response = self.client.generic('GET', '/api/action_items', json.dumps({
            'id': '123e4567-e89b-12d3-a456-426655440000',
            'client': self.first_client_id
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Object not exists.']
        })
    
    def test_get_action_item_with_invalid_id(self):
        #get actiion item with invalid id 
        response = self.client.generic('GET', '/api/action_items', json.dumps({
            'id': '50392',
            'client': self.first_client_id
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Must be a valid UUID.']
        })

    def test_patch_item_with_valid_id(self):
        #patch an action item by id 
        response = self.client.generic('PATCH', '/api/action_items', json.dumps({
            'id': self.first_action_item_id,
            'client': self.first_client_id,
            'completed': True
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_change = self.expected_action_items[0].copy()
        expected_change['completed'] = True
        self.assertEqual(response_data, expected_change)


    def test_patch_item_with_non_exist_id(self):
        #patch non-exsitent item 
        response = self.client.generic('PATCH', '/api/action_items', json.dumps({
            'id': '123e4567-e89b-12d3-a456-426655440000',
            'client': self.first_client_id,
            'completed': True
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Object not exists.']
        })
    def test_patch_item_with_invalid_id(self):
        #patch action item with invalid id
        response = self.client.generic('PATCH', '/api/action_items', json.dumps({
            'id': '12345',
            'client': self.first_client_id,
            'completed': True
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Must be a valid UUID.']
        })

    def test_delete_item_with_valid_id(self):
        #delete action item with id 
        response = self.client.generic('DELETE', '/api/action_items', json.dumps({
            'id': self.first_action_item_id,
            'client': self.first_client_id
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_change = self.expected_action_items[0]
        expected_change['id'] = None
        self.assertEqual(response_data, expected_change)

        # make sure we only have one action item left 
        response = self.client.generic('GET', '/api/action_items', json.dumps({
            'client': self.first_client_id
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, [self.expected_action_items[1]])

    def test_delete_with_non_exist_id(self):
        # delete non-existent action item
        response = self.client.generic('DELETE', '/api/action_items', json.dumps({
            'id': '123e4567-e89b-12d3-a456-426655440000',
            'client': self.first_client_id
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Object not exists.']
        })

    def test_delete_with_invalid_id(self):
        # delete with invalid id
        response = self.client.generic('DELETE', '/api/action_items', json.dumps({
            'id': '223311',
            'client': self.first_client_id
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Must be a valid UUID.']
        })
        