import json

from rest_framework import status
from rest_framework.test import APITestCase


class AdvisorAPITest(APITestCase):
    def setUp(self):
        self.expected_advisors = []
        response = self.client.post('/auth/registration', data={
            'username': 'testuser',
            'email': 'testuser@email.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.headers = response_data['key']

        # create first advisor
        response = self.client.post('/api/advisors', data={
            'first_name': 'Madison',
            'last_name': 'Montgomery',
            'email': 'm.montgomery@gmail.com',
            'phone_number': '123-333-3344'
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.first_advisor_id = response_data['id']

        # expected data return by first advisor
        self.expected_advisors.append({
            'id': self.first_advisor_id,
            'first_name': 'Madison',
            'last_name': 'Montgomery',
            'email': 'm.montgomery@gmail.com',
            'phone_number': '123-333-3344',
            'address': ''
        })

        # create second advisor
        response = self.client.post('/api/advisors', data={
            'first_name': 'Michael',
            'last_name': 'Langdon',
            'email': 'm.langdon@gmail.com',
            'phone_number': '966-666-9966',
            'address': '1120 Westchester Pl., Los Angeles CA'
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.second_advisor_id = response_data['id']

        # expected data returned by second advisor
        self.expected_advisors.append({
            'id': self.second_advisor_id,
            'first_name': 'Michael',
            'last_name': 'Langdon',
            'email': 'm.langdon@gmail.com',
            'phone_number': '966-666-9966',
            'address': '1120 Westchester Pl., Los Angeles CA'
        })

        # create client
        response = self.client.post('/api/clients', data={
            'first_name': 'Mike',
            'last_name': 'Jordan',
            'email': 'mjordan@gmail.com'
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.client_id = response_data['id']

    def test_post(self):
        response = self.client.post('/api/advisors', data={
            'first_name': 'Lana',
            'last_name': 'Winters',
            'email': 'l.winters@drexel.edu',
            'phone_number': '355-323-2233'
        }, headers=self.headers)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data, {
            'id': response_data['id'],
            'first_name': 'Lana',
            'last_name': 'Winters',
            'email': 'l.winters@drexel.edu',
            'phone_number': '355-323-2233',
            'address': ''
        })

    def test_post_assign_client_to_advisor(self):
        response = self.client.post('/api/advisors/' + self.first_advisor_id +
                                    '/clients/' + self.client_id, data={}, headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data, {
            'id': self.client_id,
            'advisor': self.first_advisor_id,
            'age': 0,
            'first_name': 'Mike',
            'last_name': 'Jordan',
            'middle_name': '',
            'birth_year': 2020,
            'email': 'mjordan@gmail.com',
            'city': 'Philadelphia',
            'state': 'PA',
            'personal_annual_net_income': '0.00',
            'additional_income': '0.00',
            'current_year': 2020,
            'total_annual_income': '0.00',
            'household_annual_net_income': '0.00',
            'total_monthly_debt_amount': '0.00'
        })

    def test_post_assign_client_to_advisor_with_invalid_id(self):
        response = self.client.post('/api/advisors/12121212' +
                                    '/clients/' + self.client_id, data={}, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_client_from_advisor(self):
        response = self.client.post('/api/advisors/' + self.first_advisor_id +
                                    '/clients/' + self.client_id, data={}, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete('/api/advisors/' + self.first_advisor_id +
                                      '/clients/' + self.client_id, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # check that the advisor field is null for client
        response = self.client.get(
            '/api/clients/' + self.client_id, headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'id': self.client_id,
            'first_name': 'Mike',
            'last_name': 'Jordan',
            'middle_name': '',
            'birth_year': 2020,
            'email': 'mjordan@gmail.com',
            'city': 'Philadelphia',
            'state': 'PA',
            'personal_annual_net_income': '0.00',
            'additional_income': '0.00',
            'current_year': 2020,
            'age': 0,
            'total_annual_income': '0.00',
            'total_monthly_debt_amount': '0.00',
            'household_annual_net_income': '0.00',
            'advisor': None
        })

        def test_delete_client_from_advisor_with_mismatched_id(self):
            response = self.client.post('/api/advisors/' + self.first_advisor_id +
                                        '/clients/' + self.client_id, data={}, headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

            response = self.client.delete('/api/advisors/' + self.second_advisor_id +
                                          '/clients/' + self.client_id, headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        def test_post_required(self):
            response = self.client.post('/api/advisors', headers=self.headers)
            response_data = json.loads(response.content)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(response_data, {
                'first_name': ['This field is required.'],
                'last_name': ['This field is required.'],
                'email': ['This field is required.'],
                'phone_number': ['This field is required.']
            })

        def test_get_list(self):
            # get the list of all advisors
            response = self.client.get('/api/advisors', headers=self.headers)
            response_data = json.loads(response.content)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response_data, {
                'count': len(self.expected_advisors),
                'next': None,
                'previous': None,
                'results': self.expected_advisors
            })

        def test_get_detail_with_valid_id(self):
            # get the advisor info with valid id
            response = self.client.get(
                '/api/advisors/' + self.first_advisor_id, headers=self.headers)
            response_data = json.loads(response.content)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response_data, self.expected_advisors[0])

        def test_get_detail_with_non_exist_id(self):
            # get non-existent advisor by id
            response = self.client.get(
                '/api/advisors/123e4567-e89b-12d3-a456-426655440000', headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_get_detail_with_invalid_id(self):
            # get advisor details with invalid id
            response = self.client.get(
                '/api/advisors/4532-122-195832', headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_patch_with_valid_id(self):
            # change advisor info with valid id
            response = self.client.patch('/api/advisors/' + self.first_advisor_id, data={
                'first_name': 'Nora',
                'email': 'n.montgomery@gmail.com'
            }, headers=self.headers)
            response_data = json.loads(response.content)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            expected_change = self.expected_advisors[0].copy()
            expected_change['first_name'] = 'Nora'
            expected_change['email'] = 'n.montgomery@gmail.com'
            self.assertEqual(response_data, expected_change)

        def test_patch_with_non_exist_id(self):
            # change advisor info with non-exist id
            response = self.client.patch('/api/advisors/123e4567-e89b-12d3-a456-426655440000', data={
                'first_name': 'Nora',
                'last_name': 'Montgomery'
            }, headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_patch_with_invalid_id(self):
            # change advisor info with invalid id
            response = self.client.patch('/api/advisors/blah12blah12blah12', data={
                'first_name': 'Nora',
                'last_name': 'Montgomery'
            }, headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_delete_with_valid_id(self):
            # delete advisor with valid id
            response = self.client.delete(
                '/api/advisors/' + self.first_advisor_id, headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

            # make sure we only have one advisor left
            response = self.client.generic(
                'GET', '/api/advisors', headers=self.headers)
            response_data = json.loads(response.content)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response_data, {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [self.expected_advisors[1]]
            })

        def test_delete_with_non_exist_id(self):
            # get non-existent advisor by id
            response = self.client.delete(
                '/api/advisors/123e4567-e89b-12d3-a456-426655440000', headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        def test_delete_with_invalid_id(self):
            # get non-existent advisor by id
            response = self.client.delete(
                '/api/advisors/123e4567asdgerr', headers=self.headers)
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
