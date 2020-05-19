import json

from rest_framework import status
from rest_framework.test import APITestCase


class ExpenseAPITest(APITestCase):
    def setUp(self):
        self.expected_expenses = []
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
            'first_name': 'Johnny',
            'last_name': 'Rose',
            'birth_year': '1990',
            'email': 'johnny.rose@gmail.com',
            'personal_annual_net_income': 100000.0,
            'additional_income': 5000.0
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.first_client_id = response_data['id']

        # create another client
        response = self.client.post('/api/clients', data={
            'first_name': 'Moira',
            'last_name': 'Rose',
            'birth_year': '1973',
            'email': 'moira.rose@gmail.com',
            'personal_annual_net_income': 15000.0,
            'additional_income': 0.0
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.second_client_id = response_data['id']

        # create expense
        response = self.client.post('/api/expenses', data={
            'client': self.first_client_id,
            'housing_type': 'Rent',
            'bills_housing': 3150.0,
            'bills_utilities': 250.0,
            'expense_shopping': 300.0,
            'expense_leisure': 500.0,
            'expense_transportation': 150.0,
            'expense_subscriptions': 50.0,
            'expense_other': 200.0,
            'current_monthly_protection_payment': 100.0,
            'current_protection_coverage': 10000.0,
            'current_retirement_savings': 25000.0
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = json.loads(response.content)
        self.expense_id = response_data['id']

        self.expected_expenses.append({
            'id': self.expense_id,
            'housing_type': 'Rent',
            'bills_housing': '3150.00',
            'bills_utilities': '250.00',
            'expense_shopping': '300.00',
            'expense_leisure': '500.00',
            'expense_transportation': '150.00',
            'expense_subscriptions': '50.00',
            'expense_other': '200.00',
            'current_monthly_protection_payment': '100.00',
            'current_protection_coverage': '10000.00',
            'current_retirement_savings': '25000.00'
        })

    def test_post(self):
        response = self.client.post('/api/expenses', data={
            'client': self.second_client_id,
            'housing_type': 'Rent',
            'bills_housing': 3150.0,
            'bills_utilities': 250.0,
            'expense_shopping': 300.0,
            'expense_leisure': 500.0,
            'expense_transportation': 150.0,
            'expense_subscriptions': 50.0,
            'expense_other': 200.0,
            'current_monthly_protection_payment': 100.0,
            'current_protection_coverage': 10000.0,
            'current_retirement_savings': 25000.0
        }, headers=self.headers)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data, {
            'id': response_data['id'],
            'housing_type': 'Rent',
            'bills_housing': '3150.00',
            'bills_utilities': '250.00',
            'expense_shopping': '300.00',
            'expense_leisure': '500.00',
            'expense_transportation': '150.00',
            'expense_subscriptions': '50.00',
            'expense_other': '200.00',
            'current_monthly_protection_payment': '100.00',
            'current_protection_coverage': '10000.00',
            'current_retirement_savings': '25000.00'
        })

    def test_post_required(self):
        response = self.client.post('/api/expenses', data={})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, {
            'client': ['This field is required.']
        })

    def test_get_list_of_expenses(self):
        # get expenses of a client
        response = self.client.get('/api/expenses', headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'count': 1,
            'next': None,
            'previous': None,
            'results': self.expected_expenses
        })

    def test_get_expenses(self):
        response = self.client.get(
            '/api/expenses/' + self.expected_expenses[0]['id'], headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_expenses[0])

    def test_get_expenses_with_valid_id(self):
        # get expenses by id
        response = self.client.get(
            '/api/expenses/' + self.expense_id, headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, self.expected_expenses[0])

    def test_get_expenses_with_non_exist_id(self):
        # get non-existent expense
        response = self.client.get(
            '/api/expenses/123e4567-e89b-12d3-a456-426655440000', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_expenses_with_invalid_id(self):
        # get expenses with invalid id
        response = self.client.get('/api/expenses/50392', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_expenses_with_valid_id(self):
        # patch a goal by id
        response = self.client.patch('/api/expenses/' + self.expense_id, data={
            'housing_type': 'Mortgage',
            'bills_housing': 4200.0
        }, headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_change = self.expected_expenses[0].copy()
        expected_change['housing_type'] = 'Mortgage'
        expected_change['bills_housing'] = '4200.00'
        self.assertEqual(response_data, expected_change)

    def test_patch_expenses_with_non_exist_id(self):
        # patch non-existent expense
        response = self.client.patch('/api/expenses/123e4567-e89b-12d3-a456-426655440000', data={
            'expense_shopping': 400.0
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_expenses_with_invalid_id(self):
        # patch expense with invalid id
        response = self.client.patch('/api/expenses/12345', data={
            'expense_shopping': 300.0
        }, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_expense_with_valid_id(self):
        # delete expense with id
        response = self.client.delete(
            '/api/expenses/' + self.expense_id, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # make sure we have only one goal now
        response = self.client.get(
            '/api/expenses?client=' + self.first_client_id, headers=self.headers)
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, {
            'count': 0,
            'next': None,
            'previous': None,
            'results': []
        })

    def test_delete_with_non_exist_id(self):
        # delete non-existent expenses
        response = self.client.delete(
            '/api/expenses/123e4567-e89b-12d3-a456-426655440000', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_with_invalid_id(self):
        # delete invalid expenses
        response = self.client.delete('/api/expenses/12345', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
