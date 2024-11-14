from django.test import TestCase
from django.db import models
from owners.models import Owner
from real_estate.models import RealEstate
from service_orders.models import (
    ENUM_Payment_Status,
    ENUM_Service_Category,
    ServiceOrder,
)
from service_orders.serializers import ServiceOrderSerializer


class ServiceOrderClass:
    def __init__(
        self,
        service_category: str,
        service_provided: str,
        price: float,
        payment_status: str,
        date_paid: str = None,
        start_date: str = None,
    ) -> None:
        self.service_category = service_category
        self.service_provided = service_provided
        self.price = price
        self.payment_status = payment_status
        self.date_paid = date_paid
        self.start_date = start_date


class TestServiceOrderModel(TestCase):
    def test_attrs(self):
        expected_attr_names = [
            "id",
            "service_category",
            "service_provided",
            "price",
            "payment_status",
            "date_paid",
            "start_date",
            "owner",
            "real_estate",
        ]

        attr_names = []
        for attr in ServiceOrder._meta.get_fields():
            if isinstance(attr, models.Field):
                attr_names.append(attr.name)

        for name in expected_attr_names:
            self.assertIn(name, attr_names)

        self.assertEqual(len(expected_attr_names), len(attr_names))

    def test_service_category_attr(self):
        service_category_field = ServiceOrder._meta.get_field(
            "service_category"
        )
        self.assertIsInstance(service_category_field, models.CharField)
        self.assertEqual(service_category_field.max_length, 13)
        self.assertEqual(
            service_category_field.choices, ENUM_Service_Category.choices
        )
        self.assertEqual(
            service_category_field.default, ENUM_Service_Category.OUTRO
        )
        self.assertEqual(service_category_field.null, False)

    def test_payment_status_attr(self):
        payment_status_field = ServiceOrder._meta.get_field("payment_status")
        self.assertIsInstance(payment_status_field, models.CharField)
        self.assertEqual(payment_status_field.max_length, 8)
        self.assertEqual(
            payment_status_field.choices, ENUM_Payment_Status.choices
        )
        self.assertEqual(
            payment_status_field.default, ENUM_Payment_Status.PENDENTE
        )
        self.assertEqual(payment_status_field.null, False)

    def test_price_attr(self):
        price_field = ServiceOrder._meta.get_field("price")
        self.assertIsInstance(price_field, models.DecimalField)
        self.assertEqual(price_field.max_digits, 10)
        self.assertEqual(price_field.decimal_places, 2)

    def test_owner_foreignkey_field(self):
        owner_field = ServiceOrder._meta.get_field("owner")
        self.assertEqual(owner_field.related_model, Owner)
        self.assertTrue(owner_field.many_to_one)
        self.assertEqual(owner_field.null, True)
        self.assertEqual(owner_field.blank, True)
        self.assertEqual(owner_field.default, None)
        self.assertEqual(
            owner_field.remote_field.related_name, "service_order_owner"
        )

    def test_real_estate_foreignkey_field(self):
        real_estate_field = ServiceOrder._meta.get_field("real_estate")
        self.assertEqual(real_estate_field.related_model, RealEstate)
        self.assertTrue(real_estate_field.many_to_one)
        self.assertEqual(real_estate_field.null, True)
        self.assertEqual(real_estate_field.blank, True)
        self.assertEqual(real_estate_field.default, None)
        self.assertEqual(
            real_estate_field.remote_field.related_name,
            "service_order_real_estate",
        )


class TestServiceOrder(TestCase):
    def setUp(self) -> None:
        self.service_order_instance = ServiceOrder.objects.create(
            service_category="Manutenção",
            service_provided="Conserto de vazamento",
            price=350.00,
            payment_status="Pendente",
            date_paid="2024-01-01T00:00:00Z",
        )

    def test_service_order_instance_attrs(self):
        service_order = ServiceOrderClass(
            "Manutenção",
            "Conserto de vazamento",
            350.00,
            "Pendente",
            "2024-01-01T00:00:00Z",
        )
        self.assertEqual(type(service_order.service_category), str)
        self.assertEqual(type(service_order.service_provided), str)
        self.assertEqual(type(service_order.price), float)
        self.assertEqual(type(service_order.payment_status), str)
        self.assertEqual(type(service_order.date_paid), str)

    def test_service_order_serializer(self):
        service_order = self.service_order_instance
        serializer = ServiceOrderSerializer(service_order)
        data = serializer.data

        self.assertEqual(data["service_category"], "Manutenção")
        self.assertEqual(data["service_provided"], "Conserto de vazamento")
        self.assertEqual(data["price"], "350.00")
        self.assertEqual(data["payment_status"], "Pendente")
        self.assertEqual(data["date_paid"], "2024-01-01T00:00:00Z")
