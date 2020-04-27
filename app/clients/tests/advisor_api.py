import json

from rest_framework import status
from rest_framework.test import APITestCase


class AdvisorAPITest(APITestCase):
    def setUp(self):
        self.expected_advisors = []

        # create first advisor
        response = self.client.generic('POST', '/api/advisors', json.dumps({
            'first_name': 'Madison',
            'last_name': 'Montgomery',
            'email': 'm.montgomery@gmail.com',
            'phone_number': '123-333-3344'
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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

        #create second advisor 
        response = self.client.generic('POST', '/api/advisors', json.dumps({
            'first_name': 'Michael',
            'last_name': 'Langdon',
            'email': 'm.langdon@gmail.com',
            'phone_number': '966-666-9966',
            'address': '1120 Westchester Pl., Los Angeles CA'
        }), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = json.loads(response.content)
        self.second_advisor_id = response_data['id']

        #expected data returned by second advisor 
        self.expected_advisors.append({
            'id': self.second_advisor_id,
            'first_name': 'Michael',
            'last_name': 'Langdon',
            'email': 'm.langdon@gmail.com',
            'phone_number': '966-666-9966',
            'address': '1120 Westchester Pl., Los Angeles CA' 
        })


    def test_post(self):
        response = self.client.generic('POST', '/api/advisors', json.dumps({
            'first_name': 'Lana',
            'last_name': 'Winters',
            'email': 'l.winters@drexel.edu',
            'phone_number': '355-323-2233'
        }), content_type='application/json')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'id': response_data['id'],
            'first_name': 'Lana',
            'last_name': 'Winters',
            'email': 'l.winters@drexel.edu',
            'phone_number': '355-323-2233',
            'address': ''
        })

    def test_post_required(self):
        response = self.client.generic(
            'POST', '/api/advisors', json.dumps({}), content_type='application/json')
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
        response = self.client.generic('GET', '/api/advisors')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_advisors)

    def test_get_detail_with_valid_id(self):
        # get the advisor info with valid id
        response = self.client.generic('GET', '/api/advisors', json.dumps({
            'id': self.first_advisor_id
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_advisors[0])   

     

    def test_get_detail_with_non_exist_id(self):
        # get non-existent advisor by id
        response = self.client.generic('GET', '/api/advisors', json.dumps({
            'id': '123e4567-e89b-12d3-a456-426655440000'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Object not exists.']
        })


    def test_get_detail_with_invalid_id(self):
        # get advisor details with invalid id
        response = self.client.generic('GET', '/api/advisors', json.dumps({
            'id': '4532-122-195832'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Must be a valid UUID.']
        })


    def test_patch_with_valid_id(self):
        # change advisor info with valid id
        response = self.client.generic('PATCH', '/api/advisors', json.dumps({
            'id': self.first_advisor_id,
            'first_name': 'Nora',
            'email': 'n.montgomery@gmail.com'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_change = self.expected_advisors[0].copy()
        expected_change['first_name'] = 'Nora'
        expected_change['email'] = 'n.montgomery@gmail.com'
        self.assertEqual(response_data, expected_change)

    def test_patch_with_non_exist_id(self):
        # change advisor info with non-exist id
        response = self.client.generic('PATCH', '/api/advisors', json.dumps({
            'id': '123e4567-e89b-12d3-a456-426655440000',
            'first_name': 'Nora',
            'last_name': 'Montgomery'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Object not exists.']
        })

    def test_patch_with_invalid_id(self):
        # change advisor info with invalid id
        response = self.client.generic('PATCH', '/api/advisors', json.dumps({
            'id': 'blah12blah12blah12',
            'first_name': 'Nora',
            'last_name': 'Montgomery'
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Must be a valid UUID.']
        })

    def test_delete_with_valid_id(self):
        # delete advisor with valid id
        response = self.client.generic('DELETE', '/api/advisors', json.dumps({
            'id': self.first_advisor_id,
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_change = self.expected_advisors[0]
        expected_change['id'] = None
        self.assertEqual(response_data, expected_change)

        # make sure we only have one advisor left
        response = self.client.generic('GET', '/api/advisors')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, [self.expected_advisors[1]])

    def test_delete_with_non_exist_id(self):
        # delete advisor with non-exist id
        response = self.client.generic('DELETE', '/api/advisors', json.dumps({
            'id': '123e4567-e89b-12d3-a456-426655440000',
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Object not exists.']
        })

    def test_delete_with_invalid_id(self):
        # delete advisor with invalid id 
        response = self.client.generic('DELETE', '/api/advisors', json.dumps({
            'id': '12blah12blah12blah',
        }), content_type='application/json')
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'id': ['Must be a valid UUID.']
        })
    

