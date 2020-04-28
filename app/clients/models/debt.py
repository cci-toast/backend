import uuid

from django.db import models

from .client import Client


class Debt(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    client = models.ForeignKey(
        to=Client,
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

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())
