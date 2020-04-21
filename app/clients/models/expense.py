import uuid
from django.db import models
from .client import Client


class Expense(models.Model):
    RENT = 'Rent'
    MORTGAGE = 'Mortgage'
    HOUSE_CHOICES = [
        (RENT, 'Rent'),
        (MORTGAGE, 'Mortgage')
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    client = models.OneToOneField(
        to=Client,
        on_delete=models.CASCADE)
    housing_type = models.CharField(
        max_length=10,
        choices=HOUSE_CHOICES,
        default=RENT)
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
    bills_insurance = models.DecimalField(
        "Bills Insurance",
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
    expense_other = models.DecimalField(
        "Expense Other",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    current_monthly_protection_payment = models.DecimalField(
        "Current Monthly Protection Payment",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    current_protection_coverage = models.DecimalField(
        "Current Protection Coverage",
        max_digits=8,
        decimal_places=2,
        default=0.0)

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())
