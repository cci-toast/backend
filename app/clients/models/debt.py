import uuid
from django.db import models
from .client import Client
from .plan import Plan
from computedfields.models import ComputedFieldsModel, computed

class Debt(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE)
    plan = models.ForeignKey(
        to=Plan,
        on_delete=models.CASCADE)
    debt_monthly_amount = models.DecimalField(
        "Debt Monthly Amount",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    debt_remaining_total = models.DecimalField(
        "Debt Remaining Total",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    debt_interest_rate = models.DecimalField(
        "Debt Interest Rate",
        max_digits=8,
        decimal_places=2,
        default=0.0)

    @computed(models.IntegerField(default=0), depends=['plan#household_annual_net_income'])
    def debt(self):
        debt_output = self.plan.household_annual_net_income * 0.36
        return debt_output

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())
