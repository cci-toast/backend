import uuid
from django.db import models


class Advisor(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    first_name = models.CharField(
        "First Name",
        max_length=240)
    last_name = models.CharField(
        "Last Name",
        max_length=240)
    email = models.EmailField(
        "Email")
    phone_number = models.CharField(
        "Phone Number",
        max_length=20)
    address = models.CharField(
        "Address",
        max_length=240,
        default="")

    def __str__(self):
        attrs = vars(self)  # pragma: no cover
        return '\n'.join('%s: %s' % item for item in attrs.items())  # pragma: no cover
