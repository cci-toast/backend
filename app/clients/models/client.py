import uuid
from django.db import models
from datetime import date
from .advisor import Advisor
from computedfields.models import ComputedFieldsModel, computed


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

    @computed(models.CharField(max_length=32, default=""))
    def combined(self):
        return u'%s %s %s' % (self.first_name, self.middle_name, self.last_name)

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())
