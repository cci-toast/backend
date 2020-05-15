import uuid
from datetime import date
from decimal import Decimal

from django.db import models

from .client import Client


class Partner(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE)
    first_name = models.CharField(
        "First Name",
        max_length=240)
    last_name = models.CharField(
        "Last Name",
        max_length=240)
    birth_year = models.IntegerField(
        "Birth Year",
        default=date.today().year)
    personal_annual_net_income = models.DecimalField(
        "Personal Annual Net Income",
        max_digits=15,
        decimal_places=2,
        default=Decimal('0.00'))

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())
