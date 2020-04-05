from django.db import models
from datetime import date
from .client import Client


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
