import uuid

from django.db import models

from .client import Client


class ActionItem(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE)
    description = models.CharField(
        "Description",
        max_length=240)
    completed = models.BooleanField(
        "Completed")

    def __str__(self):
        attrs = vars(self)
        return '\n'.join('%s: %s' % item for item in attrs.items())
