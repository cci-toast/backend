from datetime import date
from decimal import Decimal

from rest_framework.test import APITestCase

from toastapi.models import Client, Plan


class PlanComputedFieldsTest(APITestCase):
    def setUp(self):
        self.default_client = Client.objects.create(
            first_name="Potter",
            last_name="Harry",
            email="potter@gmail.com",
            personal_annual_net_income=Decimal('1000.00'))

    # tests budget_fixed_expenses
    def test_default_client_default_budget_fixed_expenses(self):
        plan = Plan.objects.create(client=self.default_client)
        self.assertEqual(plan.budget_fixed_expenses_factor, Decimal('0.50'))
        self.assertAlmostEqual(
            plan.recommended_budget_fixed_expenses_value, Decimal('41.67'), 2)

    def test_default_client_patch_budget_fixed_expenses(self):
        plan = Plan.objects.create(client=self.default_client)
        plan.budget_fixed_expenses_factor = Decimal('0.10')
        plan.save()
        self.assertEqual(plan.budget_fixed_expenses_factor, Decimal('0.10'))
        self.assertAlmostEqual(
            plan.recommended_budget_fixed_expenses_value, Decimal('8.33'), 2)

    def test_patch_client_default_budget_fixed_expenses(self):
        self.default_client.personal_annual_net_income = Decimal('32000.00')
        self.default_client.save()

        plan = Plan.objects.create(client=self.default_client)
        self.assertEqual(plan.budget_fixed_expenses_factor, Decimal('0.50'))
        self.assertAlmostEqual(
            plan.recommended_budget_fixed_expenses_value, Decimal('1333.33'), 2)

    # tests budget_savings
    def test_default_client_default_budget_savings(self):
        plan = Plan.objects.create(client=self.default_client)
        self.assertEqual(plan.budget_savings_factor, Decimal('0.20'))
        self.assertAlmostEqual(
            plan.recommended_budget_savings_value, Decimal('16.67'), 2)

    def test_default_client_patch_budget_savings(self):
        plan = Plan.objects.create(client=self.default_client)
        plan.budget_savings_factor = Decimal('0.50')
        plan.save()
        self.assertEqual(plan.budget_savings_factor, Decimal('0.50'))
        self.assertAlmostEqual(
            plan.recommended_budget_savings_value, Decimal('41.67'), 2)

    def test_patch_client_default_budget_savings(self):
        self.default_client.personal_annual_net_income = Decimal('32000.00')
        self.default_client.save()

        plan = Plan.objects.create(client=self.default_client)
        self.assertEqual(plan.budget_savings_factor, Decimal('0.20'))
        self.assertAlmostEqual(
            plan.recommended_budget_savings_value, Decimal('533.33'), 2)

    # tests budget_spending
    def test_default_client_default_budget_spending(self):
        plan = Plan.objects.create(client=self.default_client)
        self.assertEqual(plan.budget_spending_factor, Decimal('0.30'))
        self.assertAlmostEqual(
            plan.recommended_budget_spending_value, Decimal('25.00'), 2)

    def test_default_client_patch_budget_spending(self):
        plan = Plan.objects.create(client=self.default_client)
        plan.budget_spending_factor = Decimal('0.50')
        plan.save()
        self.assertEqual(plan.budget_spending_factor, Decimal('0.50'))
        self.assertAlmostEqual(
            plan.recommended_budget_spending_value, Decimal('41.67'), 2)

    def test_patch_client_default_budget_spending(self):
        self.default_client.personal_annual_net_income = Decimal('32000.00')
        self.default_client.save()

        plan = Plan.objects.create(client=self.default_client)
        self.assertEqual(plan.budget_spending_factor, Decimal('0.30'))
        self.assertAlmostEqual(
            plan.recommended_budget_spending_value, Decimal('800.00'), 2)

    # tests debt_repayment
    def test_default_client_default_monthly_maximum_debt_amount(self):
        plan = Plan.objects.create(client=self.default_client)
        self.assertEqual(plan.debt_repayment_factor, Decimal('0.36'))
        self.assertAlmostEqual(
            plan.recommended_monthly_maximum_debt_amount, Decimal('30.00'), 2)

    def test_default_client_patch_monthly_maximum_debt_amount(self):
        plan = Plan.objects.create(client=self.default_client)
        plan.debt_repayment_factor = Decimal('0.50')
        plan.save()
        self.assertEqual(
            plan.debt_repayment_factor, Decimal('0.50'))
        self.assertAlmostEqual(
            plan.recommended_monthly_maximum_debt_amount, Decimal('41.67'), 2)

    def test_patch_client_default_monthly_maximum_debt_amount(self):
        self.default_client.personal_annual_net_income = Decimal('32000.00')
        self.default_client.save()

        plan = Plan.objects.create(client=self.default_client)
        self.assertEqual(
            plan.debt_repayment_factor, Decimal('0.36'))
        self.assertAlmostEqual(
            plan.recommended_monthly_maximum_debt_amount, Decimal('960.00'), 2)

    # tests protection
    def test_default_client_default_protection(self):
        plan = Plan.objects.create(client=self.default_client)

        # client is 20 years old
        self.default_client.birth_year = date.today().year - 20
        self.default_client.save()
        plan = Plan.objects.get(client=self.default_client)
        self.assertEqual(plan.protection_factor, Decimal('20.00'))
        self.assertAlmostEqual(
            plan.recommended_protection_value, Decimal('20000.00'), 2)

        # client is 30 years old
        self.default_client.birth_year = date.today().year - 30
        self.default_client.save()
        plan = Plan.objects.get(client=self.default_client)
        self.assertEqual(plan.protection_factor, Decimal('20.00'))
        self.assertAlmostEqual(
            plan.recommended_protection_value, Decimal('20000.00'), 2)

        # client is 40 years old
        self.default_client.birth_year = date.today().year - 40
        self.default_client.save()
        plan = Plan.objects.get(client=self.default_client)
        self.assertEqual(plan.protection_factor, Decimal('12.00'))
        self.assertAlmostEqual(
            plan.recommended_protection_value, Decimal('12000.00'), 2)

        # client is 50 years old
        self.default_client.birth_year = date.today().year - 50
        self.default_client.save()
        plan = Plan.objects.get(client=self.default_client)
        self.assertEqual(plan.protection_factor, Decimal('6.00'))
        self.assertAlmostEqual(
            plan.recommended_protection_value, Decimal('6000.00'), 2)

        # client is 60 years old
        self.default_client.birth_year = date.today().year - 60
        self.default_client.save()
        plan = Plan.objects.get(client=self.default_client)
        self.assertEqual(plan.protection_factor, Decimal('6.00'))
        self.assertAlmostEqual(
            plan.recommended_protection_value, Decimal('6000.00'), 2)

    def test_patch_client_default_protection(self):
        self.default_client.personal_annual_net_income = Decimal('32000.00')
        self.default_client.birth_year = date.today().year - 60
        self.default_client.save()

        # client is 60 years old
        plan = Plan.objects.create(client=self.default_client)
        self.assertEqual(plan.protection_factor, Decimal('6.00'))
        self.assertAlmostEqual(
            plan.recommended_protection_value, Decimal('192000.00'), 2)

    # tests retirement
    def test_default_client_default_retirement(self):
        plan = Plan.objects.create(client=self.default_client)

        # client is 38 years old
        self.default_client.birth_year = date.today().year - 38
        self.default_client.save()
        plan = Plan.objects.get(client=self.default_client)
        self.assertEqual(plan.retirement_factor, Decimal('1.00'))
        self.assertAlmostEqual(
            plan.recommended_retirement_value, Decimal('1000.00'), 2)

        # client is 40 years old
        self.default_client.birth_year = date.today().year - 40
        self.default_client.save()
        plan = Plan.objects.get(client=self.default_client)
        self.assertEqual(plan.retirement_factor, Decimal('3.00'))
        self.assertAlmostEqual(
            plan.recommended_retirement_value, Decimal('3000.00'), 2)

        # client is 50 years old
        self.default_client.birth_year = date.today().year - 50
        self.default_client.save()
        plan = Plan.objects.get(client=self.default_client)
        self.assertEqual(plan.retirement_factor, Decimal('6.00'))
        self.assertAlmostEqual(
            plan.recommended_retirement_value, Decimal('6000.00'), 2)

        # client is 60 years old
        self.default_client.birth_year = date.today().year - 60
        self.default_client.save()
        plan = Plan.objects.get(client=self.default_client)
        self.assertEqual(plan.retirement_factor, Decimal('8.00'))
        self.assertAlmostEqual(
            plan.recommended_retirement_value, Decimal('8000.00'), 2)

        # client is 67 years old
        self.default_client.birth_year = date.today().year - 67
        self.default_client.save()
        plan = Plan.objects.get(client=self.default_client)
        self.assertEqual(plan.retirement_factor, Decimal('10.00'))
        self.assertAlmostEqual(
            plan.recommended_retirement_value, Decimal('10000.00'), 2)

    def test_patch_client_default_retirement(self):
        self.default_client.personal_annual_net_income = Decimal('32000.00')
        self.default_client.birth_year = date.today().year - 67
        self.default_client.save()

        # client is 67 years old
        plan = Plan.objects.create(client=self.default_client)
        self.assertEqual(plan.retirement_factor, Decimal('10.00'))
        self.assertAlmostEqual(
            plan.recommended_retirement_value, Decimal('320000.00'), 2)

    # test emergency_saving_lower_factor
    def test_default_client_default_emergency_saving_factor_lower(self):
        plan = Plan.objects.create(client=self.default_client)
        self.assertEqual(plan.emergency_savings_factor_lower, Decimal('3.00'))
        self.assertAlmostEqual(
            plan.recommended_emergency_savings_range_lower, Decimal('250.00'), 2)

    def test_default_client_patch_emergency_saving_factor_lower(self):
        plan = Plan.objects.create(client=self.default_client)
        plan.emergency_savings_factor_lower = Decimal('0.50')
        plan.save()
        self.assertEqual(
            plan.emergency_savings_factor_lower, Decimal('0.50'))
        self.assertAlmostEqual(
            plan.recommended_emergency_savings_range_lower, Decimal('41.67'), 2)

    def test_patch_client_default_emergency_saving_factor_lower(self):
        self.default_client.personal_annual_net_income = Decimal('32000.00')
        self.default_client.save()

        plan = Plan.objects.create(client=self.default_client)
        self.assertEqual(
            plan.emergency_savings_factor_lower, Decimal('3.00'))
        self.assertAlmostEqual(
            plan.recommended_emergency_savings_range_lower, Decimal('8000.00'), 2)

    # test emergency_saving_upper_factor
    def test_default_client_default_emergency_saving_factor_upper(self):
        plan = Plan.objects.create(client=self.default_client)
        self.assertEqual(plan.emergency_savings_factor_upper, Decimal('6.00'))
        self.assertAlmostEqual(
            plan.recommended_emergency_savings_range_upper, Decimal('500.00'), 2)

    def test_default_client_patch_emergency_saving_factor_upper(self):
        plan = Plan.objects.create(client=self.default_client)
        plan.emergency_savings_factor_upper = Decimal('0.50')
        plan.save()
        self.assertEqual(
            plan.emergency_savings_factor_upper, Decimal('0.50'))
        self.assertAlmostEqual(
            plan.recommended_emergency_savings_range_upper, Decimal('41.67'), 2)

    def test_patch_client_default_emergency_saving_factor_upper(self):
        self.default_client.personal_annual_net_income = Decimal('32000.00')
        self.default_client.save()

        plan = Plan.objects.create(client=self.default_client)
        self.assertEqual(
            plan.emergency_savings_factor_upper, Decimal('6.00'))
        self.assertAlmostEqual(
            plan.recommended_emergency_savings_range_upper, Decimal('16000.00'), 2)
