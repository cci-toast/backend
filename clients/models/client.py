import uuid
from datetime import date
from decimal import Decimal

from computedfields.models import ComputedFieldsModel, computed
from django.db import models

from .advisor import Advisor


class Client(ComputedFieldsModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    advisor = models.ForeignKey(
        to=Advisor,
        on_delete=models.SET_NULL,
        null=True)
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
    personal_annual_net_income = models.DecimalField(
        "Personal Annual Net Income",
        max_digits=8,
        decimal_places=2,
        default=0.0)
    additional_income = models.DecimalField(
        "Additional Income",
        max_digits=8,
        decimal_places=2,
        default=0.0)

    @computed(models.IntegerField("Current Year"), default=2020)
    def current_year(self):
        return date.today().year

    @computed(models.IntegerField("Age", default=0))
    def age(self):
        return self.current_year - self.birth_year

    @computed(models.DecimalField(
        "Total Annual Income",
        max_digits=8,
        decimal_places=2,
        default=0.0))
    def total_annual_income(self):
        return Decimal(self.personal_annual_net_income) + Decimal(self.additional_income)

    @computed(models.DecimalField(
        'Household Annual Net Income',
        max_digits=8,
        decimal_places=2,
        default=0.0),
        depends=['partner#personal_annual_net_income'])
    def household_annual_net_income(self):
        partner_income = Decimal(0.0)
        for partner in self.partner_set.all():
            partner_income = partner_income + partner.personal_annual_net_income
        return self.total_annual_income + partner_income

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())
