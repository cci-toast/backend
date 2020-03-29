from django.db import models
from datetime import date


class Advisor(models.Model):
    first_name = models.CharField(
        "First Name", 
        max_length=240)
    last_name = models.CharField(
        "Last Name", 
        max_length=240)
    email = models.EmailField(
        "Email")
    phone_number = models.CharField(
        "Phone Number",
        max_length=20)
    address = models.CharField(
        "Address",
        max_length=240,
        default="")

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())


class Client(models.Model):
    advisor = models.ForeignKey(to=Advisor, on_delete=models.SET_NULL, null=True, related_name="clients")
    first_name = models.CharField(
        "First Name", 
        max_length=240)
    last_name = models.CharField(
        "Last Name", 
        max_length=240)
    middle_name = models.CharField(
        "Middle Name",
        max_length=240,
        default="")
    birth_year = models.IntegerField(
        "Birth Year",
        default=date.today().year)
    email = models.EmailField(
        "Email")
    city = models.CharField(
        "City",
        max_length=100,
        default="Philadelphia")
    state = models.CharField(
        "State",
        max_length=100,
        default="PA")
    gross_income = models.DecimalField(
        "Gross Income",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    after_taxes_income = models.DecimalField(
        "After Taxes Income",
        max_digits=8,
        decimal_places=2,
        default=0.0)

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())


class Expense(models.Model):
    client = models.OneToOneField(to=Client, on_delete=models.CASCADE)
    bills_housing = models.DecimalField(
        "Bills Housing", 
        max_digits=8, 
        decimal_places=2, 
        default=0.0)
    bills_utilities = models.DecimalField(
        "Bills Utilities", 
        max_digits=8, 
        decimal_places=2, 
        default=0.0)
    bills_loan_or_debt = models.DecimalField(
        "Bills Loan or Debt", 
        max_digits=8, 
        decimal_places=2, 
        default=0.0)
    bills_insurance = models.DecimalField(
        "Bills Insurance", 
        max_digits=8, 
        decimal_places=2, 
        default=0.0)
    bills_other = models.DecimalField(
        "Bills Other", 
        max_digits=8, 
        decimal_places=2, 
        default=0.0)
    expense_shopping = models.DecimalField(
        "Expense Shopping", 
        max_digits=8, 
        decimal_places=2, 
        default=0.0)
    expense_leisure = models.DecimalField(
        "Expense Leisure", 
        max_digits=8, 
        decimal_places=2, 
        default=0.0)
    expense_transportation = models.DecimalField(
        "Expense Transportation", 
        max_digits=8, 
        decimal_places=2, 
        default=0.0)
    expense_subscriptions = models.DecimalField(
        "Expense Subscription", 
        max_digits=8, 
        decimal_places=2, 
        default=0.0)

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())


class Children(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    first_name = models.CharField(
        "First Name", 
        max_length=240)
    last_name = models.CharField(
        "Last Name", 
        max_length=240)
    birth_year = models.IntegerField(
        "Birth Year",
        default=date.today().year)
    planning_on_college = models.BooleanField(
        "Planning On College",
        default=False)
    in_college = models.BooleanField(
        "In College",
        default=False)

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())


class Partner(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    first_name = models.CharField(
        "First Name", 
        max_length=240)
    last_name = models.CharField(
        "Last Name", 
        max_length=240)
    birth_year = models.IntegerField(
        "Birth Year",
        default=date.today().year)
    gross_income = models.DecimalField(
        "Gross Income",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    additional_income = models.DecimalField(
        "Additional Income",
        max_digits=8,
        decimal_places=2,
        default=0.0)

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())


class Goal(models.Model):
    client = models.ForeignKey(to=Client, on_delete=models.CASCADE)
    goal_type = models.CharField(
        "Goal Type",
        max_length=240)
    goal_value = models.DecimalField(
        "Goal Value",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    goal_end_date = models.DateField(
        "Goal End Date",
        default=date.today)

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())


class Plan(models.Model):
    client = models.OneToOneField(to=Client, on_delete=models.CASCADE)
    emergency_savings_factor_upper = models.DecimalField(
        "Emergency Savings Factor Upper",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    emergency_savings_factor_lower = models.DecimalField(
        "Emergency Savings Factor Lower",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    emergency_savings_range_upper = models.DecimalField(
        "Emergency Savings Range Upper",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    emergency_savings_range_lower = models.DecimalField(
        "Emergency Savings Range Lower",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    retirement_factor = models.DecimalField(
        "Retirement Factor",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    retirement_value = models.DecimalField(
        "Retirement Value",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    budget_savings_factor = models.DecimalField(
        "Budget Savings Factor",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    budget_savings_value = models.DecimalField(
        "Budget Savings Value",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    budget_fixed_expenses_factor = models.DecimalField(
        "Budget Fixed Expenses Factor",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    budget_fixed_expenses_value = models.DecimalField(
        "Budget Fixed Expenses Value",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    budget_spending_factor = models.DecimalField(
        "Budget Spending Factor",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    budget_spending_value = models.DecimalField(
        "Budget Spending Value",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    debt_repayment_factor = models.DecimalField(
        "Debt Repayment Factor",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    debt_repayment_value = models.DecimalField(
        "Debt Repayment Value",
        max_digits=8,
        decimal_places=2,
        default=0.0)

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())
