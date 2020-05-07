import uuid
from datetime import date
from django.db import models
from .client import Client


class Goal(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE)
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
