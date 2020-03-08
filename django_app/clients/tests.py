from django.test import TestCase
from datetime import date
from decimal import Decimal
from .models import Advisor, Client, Expense, Children, Partner, Goal, Plan


class CommonSetup:
    client_first_name = "Harry"
    client_last_name = "Potter"
    client_dob = date(1993, 12, 2)
    client_email = "harrypotter@gmail.com" 
    client_zipcode = "12202"
    client_job_title = "Wizard"
    client_gross_income = Decimal("1000.00")
    client_additional_income = Decimal("2000.40")

    advisor_first_name = "John"
    advisor_last_name = "Smith"
    advisor_email = "johnsmith@gmail.com" 
    advisor_phone_number = "2344381990"


    @staticmethod
    def create_faked_client():
        client = Client.objects.create(
            first_name=CommonSetup.client_first_name,
            last_name=CommonSetup.client_last_name,
            dob=CommonSetup.client_dob,
            email=CommonSetup.client_email,
            zipcode=CommonSetup.client_zipcode,
            job_title=CommonSetup.client_job_title,
            gross_income=CommonSetup.client_gross_income,
            additional_income=CommonSetup.client_additional_income,
            advisor=None)

        return client


    @staticmethod
    def create_faked_advisor():
        advisor = Advisor.objects.create(
            first_name=CommonSetup.advisor_first_name,
            last_name=CommonSetup.advisor_last_name,
            email=CommonSetup.advisor_email,
            phone_number=CommonSetup.advisor_phone_number)

        return advisor


# Advisor tests
class AdvisorTest(TestCase):
    def setUp(self):
        CommonSetup.create_faked_advisor()


    def test_create_advisor(self):
        smith_advisor = Advisor.objects.get(email=CommonSetup.advisor_email)
        self.assertEqual(smith_advisor.first_name, CommonSetup.advisor_first_name)
        self.assertEqual(smith_advisor.last_name, CommonSetup.advisor_last_name)
        self.assertEqual(smith_advisor.email, CommonSetup.advisor_email)
        self.assertEqual(smith_advisor.phone_number, CommonSetup.advisor_phone_number)
        self.assertEqual(len(Client.objects.filter(advisor=smith_advisor.id)), 0)


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
        self.assertEqual(potter_client.first_name, CommonSetup.client_first_name)
        self.assertEqual(potter_client.last_name, CommonSetup.client_last_name)
        self.assertEqual(potter_client.dob, CommonSetup.client_dob)
        self.assertEqual(potter_client.email, CommonSetup.client_email)
        self.assertEqual(potter_client.zipcode, CommonSetup.client_zipcode)
        self.assertEqual(potter_client.gross_income, CommonSetup.client_gross_income)
        self.assertEqual(potter_client.additional_income, CommonSetup.client_additional_income)

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
            bills_loan_or_debt=Decimal("2000.00"),
            bills_insurance=Decimal("1000.00"),
            bills_other=Decimal("500.00"),
            expense_shopping=Decimal("100.00"),
            expense_leisure=Decimal("50.20"), 
            expense_transportation=Decimal("10.00"),
            expense_subscriptions=Decimal("2.00"))


    def test_create_expense(self):
        expense = Expense.objects.get(client__email=CommonSetup.client_email)
        self.assertEqual(expense.bills_housing, Decimal("4000.00"))
        self.assertEqual(expense.bills_utilities, Decimal("2000.00"))
        self.assertEqual(expense.bills_loan_or_debt, Decimal("2000.00"))
        self.assertEqual(expense.bills_insurance, Decimal("1000.00"))
        self.assertEqual(expense.bills_other, Decimal("500.00"))
        self.assertEqual(expense.expense_shopping, Decimal("100.00"))
        self.assertEqual(expense.expense_leisure, Decimal("50.20"))
        self.assertEqual(expense.expense_transportation, Decimal("10.00"))
        self.assertEqual(expense.expense_subscriptions, Decimal("2.00"))

        client = Client.objects.get(email=CommonSetup.client_email)
        self.assertEqual(expense.client, client)
        

    def test_delete_expense(self):
        expense = Expense.objects.get(client__email=CommonSetup.client_email)
        expense.delete()
        self.assertEqual(len(Expense.objects.all()), 0)
        self.assertTrue(Client.objects.filter(email=CommonSetup.client_email).exists())


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
            last_name="Weasley",
            dob=date(2000, 12, 1))

        Children.objects.create(
            client=client,
            first_name="Corona",
            last_name="Lime",
            dob=date(2020, 1, 1),
            planning_on_college=True)

    
    def test_create_children(self):
        children = Children.objects.filter(client__email=CommonSetup.client_email)
        self.assertEqual(len(children), 2)

        ron_child = children[0]
        self.assertEqual(ron_child.first_name, "Ron")
        self.assertEqual(ron_child.last_name, "Weasley")
        self.assertEqual(ron_child.dob, date(2000, 12, 1))
        self.assertFalse(ron_child.planning_on_college)
        self.assertFalse(ron_child.in_college)

        corona_child = children[1]
        self.assertEqual(corona_child.first_name, "Corona")
        self.assertEqual(corona_child.last_name, "Lime")
        self.assertEqual(corona_child.dob, date(2020, 1, 1))
        self.assertTrue(corona_child.planning_on_college)
        self.assertFalse(corona_child.in_college)


    def test_delete_children(self):
        children = Children.objects.filter(client__email=CommonSetup.client_email) 
        for child in children:
            child.delete()

        self.assertEqual(len(Children.objects.all()), 0)
        self.assertTrue(Client.objects.filter(email=CommonSetup.client_email).exists())


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
            dob=date(1991, 1, 1),
            gross_income=Decimal("12200.50"),
            additional_income=Decimal("2000.00"))


    def test_create_partner(self):
        partner = Partner.objects.filter(client__email=CommonSetup.client_email)[0]
        self.assertEqual(partner.first_name, "Putin")
        self.assertEqual(partner.last_name, "Maradona")
        self.assertEqual(partner.dob, date(1991, 1, 1))
        self.assertEqual(partner.gross_income, Decimal("12200.50"))
        self.assertEqual(partner.additional_income, Decimal("2000.00"))

        client = Client.objects.get(email=CommonSetup.client_email)
        self.assertEqual(partner.client, client)


    def test_delete_partner(self):
        partner = Partner.objects.filter(client__email=CommonSetup.client_email)[0]
        partner.delete()
        self.assertEqual(len(Partner.objects.all()), 0)
        self.assertTrue(Client.objects.filter(email=CommonSetup.client_email).exists())


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


    def test_delete_goal(self):
        goal = Goal.objects.filter(client__email=CommonSetup.client_email)[0]
        goal.delete()
        self.assertEqual(len(Goal.objects.all()), 0)
        self.assertTrue(Client.objects.filter(email=CommonSetup.client_email).exists())


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
        client = CommonSetup.create_faked_client()
        Plan.objects.create(
            client=client,
            emergency_savings_factor_upper=Decimal("4.00"),
            emergency_savings_factor_lower=Decimal("2.00"),
            emergency_savings_range_upper=Decimal("4000.00"),
            emergency_savings_range_lower=Decimal("2000.00"))

    
    def test_create_plan(self):
        plan = Plan.objects.filter(client__email=CommonSetup.client_email)[0]
        self.assertEqual(plan.emergency_savings_factor_upper, Decimal("4.00"))
        self.assertEqual(plan.emergency_savings_factor_lower, Decimal("2.00"))
        self.assertEqual(plan.emergency_savings_range_upper, Decimal("4000.00"))
        self.assertEqual(plan.emergency_savings_range_lower, Decimal("2000.00"))


    def test_delete_plan(self):
        plan = Plan.objects.filter(client__email=CommonSetup.client_email)[0]
        plan.delete()
        self.assertEqual(len(Plan.objects.all()), 0)
        self.assertTrue(Client.objects.filter(email=CommonSetup.client_email).exists())


    def test_delete_client_delete_plans(self):
        self.assertEqual(len(Client.objects.all()), 1)
        self.assertEqual(len(Plan.objects.all()), 1)

        client = Client.objects.get(email=CommonSetup.client_email)
        client.delete()
        self.assertEqual(len(Client.objects.all()), 0)
        self.assertEqual(len(Plan.objects.all()), 0)