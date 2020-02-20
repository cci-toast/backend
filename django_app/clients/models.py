from django.db import models
from datetime import date


class Client(models.Model):
    first_name = models.CharField("First Name", max_length=240)
    last_name = models.CharField("Last Name", max_length=240)
    dob = models.DateField("DOB", default=date.today)
    email = models.EmailField()
    zipcode = models.PositiveIntegerField("Zip code")
    gross_income = models.PositiveIntegerField("Gross Income")
    additional_income = models.PositiveIntegerField("Additional Income")
    job_title = models.CharField("Job Title", max_length=100)

    def __str__(self):
        return self.first_name
