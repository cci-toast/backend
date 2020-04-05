from django.db import models
from datetime import date
from .client import Client


class Children(models.Model):
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
    planning_on_college = models.BooleanField(
        "Planning On College",
        default=False)
    in_college = models.BooleanField(
        "In College",
        default=False)

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())