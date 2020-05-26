import uuid
from django.db import models
from datetime import date
from .client import Client


class Children(models.Model):
    COLLEGE = 'In College'
    GOING_TO_COLLEGE = 'Going to College'
    OTHER = 'Other'
    EDUCATION_CHOICES = [
        (COLLEGE, 'In College'),
        (GOING_TO_COLLEGE, 'Going to College'),
        (OTHER, 'Other')
    ]
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
    birth_year = models.IntegerField(
        "Birth Year",
        default=date.today().year)
    education = models.CharField(
        max_length=25,
        choices=EDUCATION_CHOICES,
        default=OTHER)

    def __str__(self):
        attrs = vars(self)  # pragma: no cover
        return '\n'.join('%s: %s' % item for item in attrs.items())  # pragma: no cover
