from datetime import date
from decimal import Decimal

from django.test import TestCase

from clients.models import (ActionItem, Advisor, Children, Client, Expense,
                            Goal, Partner, Plan)


class CommonSetup:
    client_first_name = "Harry"
    client_last_name = "Potter"
    client_birth_year = 1993
    client_email = "harrypotter@gmail.com"
    client_city = "Philadelphia"
    client_state = "PA"
    client_personal_annual_net_income = Decimal("1000.00")
    client_additional_income = Decimal("900.40")

    advisor_first_name = "John"
    advisor_last_name = "Smith"
    advisor_email = "johnsmith@gmail.com"
    advisor_phone_number = "2344381990"
    advisor_address = "123 Baring Street, Philadelphia, PA 19104"

    @staticmethod
    def create_faked_client():
        client = Client.objects.create(
            first_name=CommonSetup.client_first_name,
            last_name=CommonSetup.client_last_name,
            birth_year=CommonSetup.client_birth_year,
            email=CommonSetup.client_email,
            city=CommonSetup.client_city,
            state=CommonSetup.client_state,
            personal_annual_net_income=CommonSetup.client_personal_annual_net_income,
            additional_income=CommonSetup.client_additional_income,
            advisor=None)

        return client

    @staticmethod
    def create_faked_advisor():
        advisor = Advisor.objects.create(
            first_name=CommonSetup.advisor_first_name,
            last_name=CommonSetup.advisor_last_name,
            email=CommonSetup.advisor_email,
            phone_number=CommonSetup.advisor_phone_number,
            address=CommonSetup.advisor_address)

        return advisor


# Advisor tests
class AdvisorTest(TestCase):
    def setUp(self):
        CommonSetup.create_faked_advisor()

    def test_create_advisor(self):
        smith_advisor = Advisor.objects.get(email=CommonSetup.advisor_email)
        self.assertEqual(smith_advisor.first_name,
                         CommonSetup.advisor_first_name)
        self.assertEqual(smith_advisor.last_name,
                         CommonSetup.advisor_last_name)
        self.assertEqual(smith_advisor.email, CommonSetup.advisor_email)
        self.assertEqual(smith_advisor.phone_number,
                         CommonSetup.advisor_phone_number)
        self.assertEqual(smith_advisor.address, CommonSetup.advisor_address)
        self.assertEqual(
            len(Client.objects.filter(advisor=smith_advisor.id)), 0)

    def test_delete_advisor(self):
        smith_advisor = Advisor.objects.get(email=CommonSetup.advisor_email)
        smith_advisor.delete()
        self.assertEqual(len(Advisor.objects.all()), 0)


# Client tests
class ClientTest(TestCase):
    def setUp(self):
        advisor = CommonSetup.create_faked_advisor()
        client = CommonSetup.create_faked_client()
        advisor.client_set.add(client)

    def test_create_client(self):
        potter_client = Client.objects.get(email=CommonSetup.client_email)
        self.assertEqual(potter_client.first_name,
                         CommonSetup.client_first_name)
        self.assertEqual(potter_client.last_name, CommonSetup.client_last_name)
        self.assertEqual(potter_client.middle_name, "")
        self.assertEqual(potter_client.birth_year,
                         CommonSetup.client_birth_year)
        self.assertEqual(potter_client.email, CommonSetup.client_email)
        self.assertEqual(potter_client.city, CommonSetup.client_city)
        self.assertEqual(potter_client.state, CommonSetup.client_state)
        self.assertEqual(potter_client.personal_annual_net_income,
                         CommonSetup.client_personal_annual_net_income)
        self.assertEqual(potter_client.additional_income,
                         CommonSetup.client_additional_income)
        self.assertEqual(potter_client.household_annual_net_income,
                         potter_client.total_annual_income)

        john_advisor = Advisor.objects.get(email=CommonSetup.advisor_email)
        client_set = john_advisor.client_set.all()
        self.assertEqual(client_set[0], potter_client)

    def test_delete_client(self):
        potter_client = Client.objects.get(email=CommonSetup.client_email)
        potter_client.delete()
        self.assertEqual(len(Client.objects.all()), 0)

        john_advisor = Advisor.objects.get(email=CommonSetup.advisor_email)
        client_set = john_advisor.client_set.all()
        self.assertEqual(len(client_set), 0)

    def test_delete_advisor_client_not_delete(self):
        john_advisor = Advisor.objects.get(email=CommonSetup.advisor_email)
        john_advisor.delete()
        self.assertEqual(len(Advisor.objects.all()), 0)

        potter_client = Client.objects.get(email=CommonSetup.client_email)
        self.assertEqual(potter_client.advisor, None)


# Expense tests
class ExpenseTest(TestCase):
    def setUp(self):
        client = CommonSetup.create_faked_client()

        Expense.objects.create(
            client=client,
            bills_housing=Decimal("4000.00"),
            bills_utilities=Decimal("2000.00"),
            expense_shopping=Decimal("100.00"),
            expense_leisure=Decimal("50.20"),
            expense_transportation=Decimal("10.00"),
            expense_subscriptions=Decimal("2.00"),
            expense_other=Decimal("500.00"),
            current_monthly_protection_payment=Decimal("100.00"),
            current_protection_coverage=Decimal("200.00"))

    def test_create_expense(self):
        expense = Expense.objects.get(client__email=CommonSetup.client_email)
        self.assertEqual(expense.housing_type, expense.RENT)
        self.assertEqual(expense.bills_housing, Decimal("4000.00"))
        self.assertEqual(expense.bills_utilities, Decimal("2000.00"))
        self.assertEqual(expense.expense_shopping, Decimal("100.00"))
        self.assertEqual(expense.expense_leisure, Decimal("50.20"))
        self.assertEqual(expense.expense_transportation, Decimal("10.00"))
        self.assertEqual(expense.expense_subscriptions, Decimal("2.00"))
        self.assertEqual(expense.expense_other, Decimal("500.00"))
        self.assertEqual(
            expense.current_monthly_protection_payment, Decimal("100.00"))
        self.assertEqual(expense.current_protection_coverage,
                         Decimal("200.00"))

        client = Client.objects.get(email=CommonSetup.client_email)
        self.assertEqual(expense.client, client)

    def test_delete_expense(self):
        expense = Expense.objects.get(client__email=CommonSetup.client_email)
        expense.delete()
        self.assertEqual(len(Expense.objects.all()), 0)
        self.assertTrue(Client.objects.filter(
            email=CommonSetup.client_email).exists())

    def test_delete_client_delete_expense(self):
        self.assertEqual(len(Client.objects.all()), 1)
        self.assertEqual(len(Expense.objects.all()), 1)

        client = Client.objects.get(email=CommonSetup.client_email)
        client.delete()
        self.assertEqual(len(Client.objects.all()), 0)
        self.assertEqual(len(Expense.objects.all()), 0)


# Children tests
class ChildrenTest(TestCase):
    def setUp(self):
        client = CommonSetup.create_faked_client()

        Children.objects.create(
            client=client,
            first_name="Ron",
            birth_year=2000,
            education=Children.GOING_TO_COLLEGE)

        Children.objects.create(
            client=client,
            first_name="Corona",
            birth_year=2020,
            education=Children.OTHER)

    def test_create_children(self):
        children = Children.objects.filter(
            client__email=CommonSetup.client_email)
        self.assertEqual(len(children), 2)

        ron_child = children[0]
        self.assertEqual(ron_child.first_name, "Ron")
        self.assertEqual(ron_child.birth_year, 2000)
        self.assertEqual(ron_child.education, "Going to College")

        corona_child = children[1]
        self.assertEqual(corona_child.first_name, "Corona")
        self.assertEqual(corona_child.birth_year, 2020)
        self.assertEqual(corona_child.education, "Other")

    def test_delete_children(self):
        children = Children.objects.filter(
            client__email=CommonSetup.client_email)
        for child in children:
            child.delete()

        self.assertEqual(len(Children.objects.all()), 0)
        self.assertTrue(Client.objects.filter(
            email=CommonSetup.client_email).exists())

    def test_delete_client_delete_children(self):
        self.assertEqual(len(Client.objects.all()), 1)
        self.assertEqual(len(Children.objects.all()), 2)

        client = Client.objects.get(email=CommonSetup.client_email)
        client.delete()
        self.assertEqual(len(Client.objects.all()), 0)
        self.assertEqual(len(Children.objects.all()), 0)


# Partner tests
class PartnerTest(TestCase):
    def setUp(self):
        client = CommonSetup.create_faked_client()
        Partner.objects.create(
            client=client,
            first_name="Putin",
            last_name="Maradona",
            birth_year=1991,
            personal_annual_net_income=Decimal("12200.50"))

    def test_create_partner(self):
        partner = Partner.objects.filter(
            client__email=CommonSetup.client_email)[0]
        self.assertEqual(partner.first_name, "Putin")
        self.assertEqual(partner.last_name, "Maradona")
        self.assertEqual(partner.birth_year, 1991)
        self.assertEqual(partner.personal_annual_net_income,
                         Decimal("12200.50"))

        client = Client.objects.get(email=CommonSetup.client_email)
        self.assertEqual(partner.client, client)

    def test_delete_partner(self):
        partner = Partner.objects.filter(
            client__email=CommonSetup.client_email)[0]
        partner.delete()
        self.assertEqual(len(Partner.objects.all()), 0)
        self.assertTrue(Client.objects.filter(
            email=CommonSetup.client_email).exists())

    def test_delete_client_delete_partners(self):
        self.assertEqual(len(Client.objects.all()), 1)
        self.assertEqual(len(Partner.objects.all()), 1)

        client = Client.objects.get(email=CommonSetup.client_email)
        client.delete()
        self.assertEqual(len(Client.objects.all()), 0)
        self.assertEqual(len(Partner.objects.all()), 0)


# Goal tests
class GoalTest(TestCase):
    def setUp(self):
        client = CommonSetup.create_faked_client()
        Goal.objects.create(
            client=client,
            goal_type="Save Car",
            goal_value=Decimal("2000.00"))

    def test_create_goal(self):
        goal = Goal.objects.filter(client__email=CommonSetup.client_email)[0]
        self.assertEqual(goal.goal_type, "Save Car")
        self.assertEqual(goal.goal_value, Decimal("2000.00"))
        self.assertEqual(goal.goal_end_date, date.today())

    def test_delete_goal(self):
        goal = Goal.objects.filter(client__email=CommonSetup.client_email)[0]
        goal.delete()
        self.assertEqual(len(Goal.objects.all()), 0)
        self.assertTrue(Client.objects.filter(
            email=CommonSetup.client_email).exists())

    def test_delete_client_delete_goals(self):
        self.assertEqual(len(Client.objects.all()), 1)
        self.assertEqual(len(Goal.objects.all()), 1)

        client = Client.objects.get(email=CommonSetup.client_email)
        client.delete()
        self.assertEqual(len(Client.objects.all()), 0)
        self.assertEqual(len(Goal.objects.all()), 0)


# Plan tests
class PlanTest(TestCase):
    def setUp(self):
        self.client = CommonSetup.create_faked_client()
        Plan.objects.create(
            client=self.client,
            emergency_savings_factor_upper=Decimal("4.00"),
            emergency_savings_factor_lower=Decimal("2.00"))

    def test_create_plan(self):
        plan = Plan.objects.filter(client__email=CommonSetup.client_email)[0]
        self.assertEqual(plan.debt_repayment_factor, Decimal("0.36"))
        self.assertEqual(plan.protection_factor, Decimal("20.00"))
        self.assertEqual(plan.emergency_savings_factor_upper, Decimal("4.00"))
        self.assertEqual(plan.emergency_savings_factor_lower, Decimal("2.00"))
        self.assertEqual(plan.retirement_factor, Decimal("1.0"))
        self.assertEqual(plan.budget_savings_factor, Decimal("0.2"))
        self.assertEqual(plan.budget_fixed_expenses_factor, Decimal("0.5"))
        self.assertEqual(plan.budget_spending_factor, Decimal("0.3"))
        self.assertEqual(plan.recommended_protection_value, Decimal("3167.33"))
        self.assertEqual(
            plan.recommended_budget_savings_value, Decimal("31.67"))
        self.assertEqual(
            plan.recommended_budget_fixed_expenses_value, Decimal("79.18"))
        self.assertEqual(
            plan.recommended_budget_spending_value, Decimal("47.51"))
        self.assertEqual(
            plan.recommended_retirement_value, self.client.total_annual_income)
        self.assertEqual(
            plan.recommended_emergency_savings_range_upper, Decimal("633.47"))
        self.assertEqual(
            plan.recommended_emergency_savings_range_lower, Decimal("316.73"))
        self.assertEqual(
            plan.recommended_monthly_maximum_debt_amount, Decimal("57.01"))

    def test_delete_plan(self):
        plan = Plan.objects.filter(client__email=CommonSetup.client_email)[0]
        plan.delete()
        self.assertEqual(len(Plan.objects.all()), 0)
        self.assertTrue(Client.objects.filter(
            email=CommonSetup.client_email).exists())

    def test_delete_client_delete_plans(self):
        self.assertEqual(len(Client.objects.all()), 1)
        self.assertEqual(len(Plan.objects.all()), 1)

        client = Client.objects.get(email=CommonSetup.client_email)
        client.delete()
        self.assertEqual(len(Client.objects.all()), 0)
        self.assertEqual(len(Plan.objects.all()), 0)


# Action item tests
class ActionItemTest(TestCase):
    def setUp(self):
        client = CommonSetup.create_faked_client()
        ActionItem.objects.create(
            client=client,
            description="Buy a house for me",
            completed=False)

    def test_create_action_item(self):
        action_item = ActionItem.objects.filter(
            client__email=CommonSetup.client_email)[0]
        self.assertEqual(action_item.description, "Buy a house for me")
        self.assertEqual(action_item.completed, False)

    def test_delete_action_item(self):
        action_item = ActionItem.objects.filter(
            client__email=CommonSetup.client_email)[0]
        action_item.delete()
        self.assertEqual(len(ActionItem.objects.all()), 0)
        self.assertTrue(Client.objects.filter(
            email=CommonSetup.client_email).exists())

    def test_delete_client_delete_action_items(self):
        self.assertEqual(len(ActionItem.objects.all()), 1)
        self.assertEqual(len(ActionItem.objects.all()), 1)

        client = Client.objects.get(email=CommonSetup.client_email)
        client.delete()
        self.assertEqual(len(Client.objects.all()), 0)
        self.assertEqual(len(ActionItem.objects.all()), 0)
