import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=240, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=240, verbose_name='Last Name')),
                ('dob', models.DateField(default=datetime.date.today, verbose_name='DOB')),
                ('email', models.EmailField(max_length=254)),
                ('zipcode', models.PositiveIntegerField(verbose_name='Zip code')),
                ('gross_income', models.PositiveIntegerField(verbose_name='Gross Income')),
                ('additional_income', models.PositiveIntegerField(verbose_name='Additional Income')),
                ('job_title', models.CharField(max_length=100, verbose_name='Job Title')),
            ],
        ),
    ]