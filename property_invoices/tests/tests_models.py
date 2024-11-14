from django.test import TestCase
from django.db import models
from clients.models import Client
from property_invoices.models import (
    ENUM_Months_Of_Year,
    ENUM_Status_Of_Invoice,
    PropertyInvoice,
)
from property_invoices.serializers import PropertyInvoiceSerializer
from real_estate.models import RealEstate


class PropertyInvoiceClass:
    def __init__(
        self,
        month: str,
        due_date: int,
        rental_value: int,
        status_invoice: str,
        date_it_was_paid: str,
        observations: str,
    ) -> None:
        self.month = month
        self.due_date = due_date
        self.rental_value = rental_value
        self.status_invoice = status_invoice
        self.date_it_was_paid = date_it_was_paid
        self.observations = observations


class TestPropertyInvoiceModel(TestCase):
    def test_attrs(self):
        expected_attr_names = [
            "id",
            "month",
            "due_date",
            "rental_value",
            "status_invoice",
            "date_it_was_paid",
            "observations",
            "client",
            "real_estate",
        ]

        attr_names = []
        for attr in PropertyInvoice._meta.get_fields():
            if isinstance(attr, models.Field):
                attr_names.append(attr.name)

        for name in expected_attr_names:
            self.assertIn(name, attr_names)

        self.assertEqual(len(expected_attr_names), len(attr_names))

    def test_name_attr(self):
        month_field = PropertyInvoice._meta.get_field("month")
        self.assertIsInstance(month_field, models.CharField)
        self.assertEqual(month_field.max_length, 9)
        self.assertEqual(month_field.choices, ENUM_Months_Of_Year.choices)
        self.assertEqual(month_field.null, False)

        due_date_field = PropertyInvoice._meta.get_field("due_date")
        self.assertIsInstance(due_date_field, models.PositiveIntegerField)
        self.assertEqual(due_date_field.null, False)

        rental_value_field = PropertyInvoice._meta.get_field("rental_value")
        self.assertIsInstance(rental_value_field, models.PositiveIntegerField)
        self.assertEqual(rental_value_field.null, False)

        status_invoice_field = PropertyInvoice._meta.get_field(
            "status_invoice"
        )
        self.assertIsInstance(status_invoice_field, models.CharField)
        self.assertEqual(status_invoice_field.max_length, 8)
        self.assertEqual(
            status_invoice_field.choices, ENUM_Status_Of_Invoice.choices
        )
        self.assertEqual(
            status_invoice_field.default, ENUM_Status_Of_Invoice.PENDENTE
        )
        self.assertEqual(status_invoice_field.null, False)

        date_it_was_paid_field = PropertyInvoice._meta.get_field(
            "date_it_was_paid"
        )
        self.assertIsInstance(date_it_was_paid_field, models.DateTimeField)
        self.assertEqual(date_it_was_paid_field.null, True)
        self.assertEqual(date_it_was_paid_field.blank, True)

        observations_field = PropertyInvoice._meta.get_field("observations")
        self.assertIsInstance(observations_field, models.CharField)
        self.assertEqual(observations_field.max_length, 255)
        self.assertEqual(observations_field.null, True)
        self.assertEqual(observations_field.blank, True)

    def test_property_invoice_to_client_foreignkey_field(self):
        client_field = PropertyInvoice._meta.get_field("client")
        self.assertEqual(client_field.related_model, Client)
        self.assertTrue(client_field.many_to_one)
        self.assertEqual(client_field.null, True)
        self.assertEqual(client_field.blank, True)
        self.assertEqual(client_field.default, None)

    def test_property_invoice_to_real_estate_foreignkey_field(self):
        real_estate_field = PropertyInvoice._meta.get_field("real_estate")
        self.assertEqual(real_estate_field.related_model, RealEstate)
        self.assertTrue(real_estate_field.many_to_one)
        self.assertEqual(real_estate_field.null, True)
        self.assertEqual(real_estate_field.blank, True)
        self.assertEqual(real_estate_field.default, None)


class TestPropertyInvoice(TestCase):
    def setUp(self) -> None:
        self.invoice_create = PropertyInvoice.objects.create(
            month="Janeiro",
            due_date=10,
            rental_value=1000,
            status_invoice="Pendente",
            date_it_was_paid=None,
            observations="Pagamento pendente",
        )

    def test_property_invoice_instance_attrs(self):
        invoice = PropertyInvoiceClass(
            "Janeiro",
            10,
            1000,
            "Pendente",
            None,
            "Pagamento pendente",
        )
        self.assertEqual(type(invoice.month), str)
        self.assertEqual(type(invoice.due_date), int)
        self.assertEqual(type(invoice.rental_value), int)
        self.assertEqual(type(invoice.status_invoice), str)
        self.assertIn(invoice.status_invoice, ENUM_Status_Of_Invoice.values)
        self.assertEqual(type(invoice.observations), str)

    def test_property_invoice_serializer(self):
        invoice = self.invoice_create
        serializer = PropertyInvoiceSerializer(invoice)
        data = serializer.data

        self.assertEqual(data["month"], "Janeiro")
        self.assertEqual(data["due_date"], 10)
        self.assertEqual(data["rental_value"], 1000)
        self.assertEqual(data["status_invoice"], "Pendente")
        self.assertEqual(data["date_it_was_paid"], None)
        self.assertEqual(data["observations"], "Pagamento pendente")
