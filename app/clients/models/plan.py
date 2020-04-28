import uuid
from datetime import date

from django.db import models

from .client import Client


class Plan(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    client = models.OneToOneField(
        to=Client,
        on_delete=models.CASCADE)
    protection_factor_upper = models.DecimalField(
        "Protection Factor Upper",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    protection_factor_lower = models.DecimalField(
        "Protection Factor Lower",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    protection_range_upper = models.DecimalField(
        "Protection Range Upper",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    protection_range_lower = models.DecimalField(
        "Protection Range Lower",
        max_digits=8,
        decimal_places=2,
        default=0.0)
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
    household_annual_net_income = models.DecimalField(
        "Household Annual Net Income",
        max_digits=8,
        decimal_places=2,
        default=0.0)

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())
