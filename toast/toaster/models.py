from django.db import models

# Create your models here.
class Toaster(models.Model):
    name = models.CharField(max_length=120)
    income = models.PositiveIntegerField()
    age = models.PositiveIntegerField()

def _str_(self):
    return self.name
