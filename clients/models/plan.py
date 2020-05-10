import uuid
from decimal import Decimal

from computedfields.models import ComputedFieldsModel, computed
from django.db import models

from .client import Client


# We would leave the factor fields alone since they're basically configurable constants We need to change the value
# and range fields to @computed based on client.birth_year and client.annual_net_income + client.additional_income


class Plan(ComputedFieldsModel):
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
        default=6.0)
    emergency_savings_factor_lower = models.DecimalField(
        "Emergency Savings Factor Lower",
        max_digits=8,
        decimal_places=2,
        default=3.0)
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
        default=0.36)

    @computed(models.DecimalField(
        'Retirement Factor',
        max_digits=5,
        decimal_places=2,
        default=1.0), depends=['client#age'])
    def retirement_factor(self):
        client_age = self.client.age
        if client_age < 39:
            return 1.0
        if 40 <= client_age <= 49:
            return 3.0
        if 50 <= client_age <= 59:
            return 6.0
        if 60 <= client_age <= 66:
            return 8.0
        if client_age >= 67:
            return 10.0
        return 1.0

    # Recommended Retirement 
    @computed(models.DecimalField(
        'Recommended Retirement Value',
        max_digits=8,
        decimal_places=2,
        default=0.0), depends=['client#total_annual_income'])
    def recommended_retirement_value(self):
        return Decimal(self.retirement_factor) * self.client.total_annual_income

    # Recommended Debt
    @computed(models.DecimalField(
        'Recommended Monthly Maximum Debt Amount',
        max_digits=8,
        decimal_places=2,
        default=0.0), depends=['client#total_annual_net_income'])
    def recommended_monthly_maximum_debt_amount(self):
        return Decimal(self.client.total_annual_income) * Decimal(self.debt_repayment_factor) / 12.0

    # Recommended emergency savings upper range
    @computed(models.DecimalField(
        'Recommended Emergency Savings Range Upper',
        max_digits=8,
        decimal_places=2,
        default=0.0), depends=['client#total_annual_net_income'])
    def recommended_emergency_savings_range_upper(self):
        return Decimal((self.client.total_annual_income / 12) * Decimal(self.emergency_savings_factor_upper))

    # Recommended emergency savings lower range
    @computed(models.DecimalField(
        'Recommended Emergency Savings Range Lower',
        max_digits=8,
        decimal_places=2,
        default=0.0), depends=['client#total_annual_net_income'])
    def recommended_emergency_savings_range_lower(self):
        return Decimal((self.client.total_annual_income / 12) * Decimal(self.emergency_savings_factor_lower))

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())
