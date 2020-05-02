import json

from rest_framework import status
from rest_framework.test import APITestCase


class ClientAPITest(APITestCase):
    def setUp(self):
        self.expected_action_items = []
    
    #create a client 
    response = self.client.generic('POST', '/api/clients', json.dumps({
            'first_name': 'Kai',
            'last_name': 'Anderson',
            'birth_year': '1990',
            'email': 'kai.anderson@gmail.com',
            'personal_annual_net_income': 800000.0,
            'additional_income': 10000.0,
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.first_client_id = response_data['id']

    #create first action item 
    response = self.client.generic('POST', '/api/action_items', json.dumps({
            'client': self.first_client_id,
            'description': 'Set aside $1,600 for emergency savings',
            'completed': 0
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.first_action_item_id = response_data['id']

    response = self.client.generic('POST', '/api/action_items', json.dumps({
            'client': self.first_client_id,
            'description': 'Set aside $500 to repay debt this month',
            'completed': 1
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.second_action_item_id = response_data['id']

    #create second action item



        