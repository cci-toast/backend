import json

from rest_framework import status
from rest_framework.test import APITestCase


class AdvisorAPITest(APITestCase):
    def setUp(self):
        self.expected_advisors = []

        # create first advisor
        response = self.client.post('/api/advisors', data={
            'first_name': 'Madison',
            'last_name': 'Montgomery',
            'email': 'm.montgomery@gmail.com',
            'phone_number': '123-333-3344'
        })
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
        })
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

    def test_post(self):
        response = self.client.post('/api/advisors', data={
            'first_name': 'Lana',
            'last_name': 'Winters',
            'email': 'l.winters@drexel.edu',
            'phone_number': '355-323-2233'
        })
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

    def test_post_required(self):
        response = self.client.post('/api/advisors')
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
        response = self.client.get('/api/advisors')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_advisors)

    def test_get_detail_with_valid_id(self):
        # get the advisor info with valid id
        response = self.client.get('/api/advisors/' + self.first_advisor_id)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_advisors[0])

    def test_get_detail_with_non_exist_id(self):
        # get non-existent advisor by id
        response = self.client.get(
            '/api/advisors/123e4567-e89b-12d3-a456-426655440000')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_detail_with_invalid_id(self):
        # get advisor details with invalid id
        response = self.client.get('/api/advisors/4532-122-195832')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_with_valid_id(self):
        # change advisor info with valid id
        response = self.client.patch('/api/advisors/' + self.first_advisor_id, data={
            'first_name': 'Nora',
            'email': 'n.montgomery@gmail.com'
        })
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
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_with_invalid_id(self):
        # change advisor info with invalid id
        response = self.client.patch('/api/advisors/blah12blah12blah12', data={
            'first_name': 'Nora',
            'last_name': 'Montgomery'
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_valid_id(self):
        # delete advisor with valid id
        response = self.client.delete('/api/advisors/' + self.first_advisor_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # make sure we only have one advisor left
        response = self.client.generic('GET', '/api/advisors')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, [self.expected_advisors[1]])

    def test_delete_with_non_exist_id(self):
        # get non-existent advisor by id
        response = self.client.delete(
            '/api/advisors/123e4567-e89b-12d3-a456-426655440000')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_invalid_id(self):
        # get non-existent advisor by id
        response = self.client.delete(
            '/api/advisors/123e4567asdgerr')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
