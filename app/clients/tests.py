from django.test import TestCase
from datetime import date
from decimal import *
from .models import Advisor, Client


# Advisor tests 
class AdvisorTest(TestCase):
    def setUp(self):
        Advisor.objects.create(
            first_name="John",
            last_name="Smith",
            email="johnsmith@gmail.com",
            phone_number="2344381990",
            address="123 Baring Street",
            city="Philadelphia",
            zipcode="19104",
            state="PA")


    def test_create_advisor(self):
        smith_advisor = Advisor.objects.get(email="johnsmith@gmail.com")
        self.assertEqual(smith_advisor.first_name, "John")
        self.assertEqual(smith_advisor.last_name, "Smith")
        self.assertEqual(smith_advisor.email, "johnsmith@gmail.com")
        self.assertEqual(smith_advisor.phone_number, "2344381990")
        self.assertEqual(smith_advisor.address, "123 Baring Street")
        self.assertEqual(smith_advisor.city, "Philadelphia")
        self.assertEqual(smith_advisor.zipcode, "19104")
        self.assertEqual(smith_advisor.state, "PA")
        self.assertEqual(len(Client.objects.filter(advisor=smith_advisor.id)), 0)


    def test_delete_advisor(self):
        smith_advisor = Advisor.objects.get(email="johnsmith@gmail.com")
        smith_advisor.delete()
        self.assertEqual(len(Advisor.objects.all()), 0)


# Client tests
class ClientTest(TestCase):
    def setUp(self):
        self.john_advisor = Advisor.objects.create(
            first_name="John",
            last_name="Smith",
            email="johnsmith@gmail.com",
            phone_number="2344381990",
            address="123 Baring Street",
            city="Philadelphia",
            zipcode="19104",
            state="PA")

        self.potter_client = Client.objects.create(
            first_name="Harry",
            last_name="Potter",
            dob= date(1993, 12, 2),
            email="harrypotter@gmail.com",
            zipcode="12202",
            job_title="Wizard",
            gross_income=Decimal("1000.00"),
            additional_income=Decimal("20000.40"),
            advisor=self.john_advisor)


    def test_create_client(self):
        self.assertEqual(self.potter_client.first_name, "Harry")
        self.assertEqual(self.potter_client.middle_name, "James")
        self.assertEqual(self.potter_client.last_name, "Potter")
        self.assertEqual(self.potter_client.birth_year, "1996")
        self.assertEqual(self.potter_client.email, "harrypotter@gmail.com")
        self.assertEqual(self.potter_client.city, "London")
        self.assertEqual(self.potter_client.state, "UK")
        self.assertEqual(self.potter_client.gross_income, Decimal("1000.00"))
        self.assertEqual(self.potter_client.additional_income, Decimal("20000.40"))

    
    def test_delete_client(self):
        pass