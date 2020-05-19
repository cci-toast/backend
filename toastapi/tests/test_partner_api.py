import json

from rest_framework import status
from rest_framework.test import APITestCase


class PartnerAPITest(APITestCase):
    def setUp(self):
        self.expected_partners = []
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
            'first_name': 'Alexis',
            'last_name': 'Rose',
            'birth_year': '1992',
            'email': 'alexis.schitt@gmail.com',
            'personal_annual_net_income': 127000.0,
            'additional_income': 23000.0
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.first_client_id = response_data['id']

        # first client: create partner
        response = self.client.post('/api/partner', data={
            'client': self.first_client_id,
            'first_name': 'Ted',
            'last_name': 'Mullens',
            'birth_year': '1989',
            'personal_annual_net_income': 100000.0
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.partner_id = response_data['id']

        self.expected_partners.append({
            'id': self.partner_id,
            'first_name': 'Ted',
            'last_name': 'Mullens',
            'birth_year': 1989,
            'personal_annual_net_income': '100000.00'
        })

    def test_post(self):
        response = self.client.post('/api/partner', data={
            'client': self.first_client_id,
            'first_name': 'Ted',
            'last_name': 'Mullens',
            'birth_year': '1989',
            'personal_annual_net_income': 100000.0
        }, headers=self.headers)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data, {
            'id': response_data['id'],
            'first_name': 'Ted',
            'last_name': 'Mullens',
            'birth_year': 1989,
            'personal_annual_net_income': '100000.00'
        })

    def test_post_required(self):
        response = self.client.post('/api/partner', data={})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'first_name': ['This field is required.'],
            'last_name': ['This field is required.'],
            'client': ['This field is required.']
        })

    def test_get_list_of_partners(self):
        # get all partners for a client
        response = self.client.get('/api/partner', headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'count': 1,
            'next': None,
            'previous': None,
            'results': self.expected_partners
        })

    def test_get_partner(self):
        response = self.client.get(
            '/api/partner/' + self.expected_partners[0]['id'], headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_partners[0])

    def test_get_partner_with_valid_id(self):
        # get partner item by id
        response = self.client.get(
            '/api/partner/' + self.partner_id, headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_partners[0])

    def test_get_partner_with_non_exist_id(self):
        # get non-existent partner
        response = self.client.get(
            '/api/partner/123e4567-e89b-12d3-a456-426655440000', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_partner_with_invalid_id(self):
        # get partner with invalid id
        response = self.client.get('/api/partner/50392', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_partner_with_valid_id(self):
        # patch an action item by id
        response = self.client.patch('/api/partner/' + self.partner_id, data={
            'personal_annual_net_income': 200000.0
        }, headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_change = self.expected_partners[0].copy()
        expected_change['personal_annual_net_income'] = '200000.00'
        self.assertEqual(response_data, expected_change)

    def test_patch_partner_with_non_exist_id(self):
        # patch non-existent partner
        response = self.client.patch('/api/partner/123e4567-e89b-12d3-a456-426655440000', data={
            'personal_annual_net_income': 200000.0
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_partner_with_invalid_id(self):
        # patch partner with invalid id
        response = self.client.patch('/api/partner/12345', data={
            'personal_annual_net_income': 200000.0
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_partner_with_valid_id(self):
        # delete partner with id
        response = self.client.delete(
            '/api/partner/' + self.partner_id, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # make sure we have no partner assigned to client
        response = self.client.get(
            '/api/partner?client=' + self.first_client_id, headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        })

    def test_delete_with_non_exist_id(self):
        # delete non-existent partner
        response = self.client.delete(
            '/api/partner/123e4567-e89b-12d3-a456-426655440000', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_invalid_id(self):
        # delete non-existent partner
        response = self.client.delete('/api/partner/12345', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
