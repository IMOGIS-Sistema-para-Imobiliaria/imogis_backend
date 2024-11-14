from django.test import TestCase
from django.db import models
from clients.models import Client
from owners.models import Owner
from bonus_and_transfer.models import BonusAndTransfer
from bonus_and_transfer.serializers import BonusAndTransferSerializer


class BonusAndTransferClass:
    def __init__(
        self,
        sales_bonus: float,
        profit_transfer: int,
    ) -> None:
        self.sales_bonus = sales_bonus
        self.profit_transfer = profit_transfer


class TestBonusAndTransferModel(TestCase):
    def test_attrs(self):
        expected_attr_names = [
            "id",
            "sales_bonus",
            "profit_transfer",
            "owner",
            "client",
        ]

        attr_names = []
        for attr in BonusAndTransfer._meta.get_fields():
            if isinstance(attr, models.Field):
                attr_names.append(attr.name)

        for name in expected_attr_names:
            self.assertIn(name, attr_names)

        self.assertEqual(len(expected_attr_names), len(attr_names))

    def test_sales_bonus_attr(self):
        sales_bonus_field = BonusAndTransfer._meta.get_field("sales_bonus")
        self.assertIsInstance(sales_bonus_field, models.DecimalField)
        self.assertEqual(sales_bonus_field.max_digits, 10)
        self.assertEqual(sales_bonus_field.decimal_places, 2)
        self.assertEqual(sales_bonus_field.null, False)

    def test_profit_transfer_attr(self):
        profit_transfer_field = BonusAndTransfer._meta.get_field(
            "profit_transfer"
        )
        self.assertIsInstance(profit_transfer_field, models.DecimalField)
        self.assertEqual(profit_transfer_field.max_digits, 10)
        self.assertEqual(profit_transfer_field.decimal_places, 0)
        self.assertEqual(profit_transfer_field.null, False)

    def test_bonus_and_transfer_to_owner_foreignkey_field(self):
        owner_field = BonusAndTransfer._meta.get_field("owner")
        self.assertEqual(owner_field.related_model, Owner)
        self.assertTrue(owner_field.many_to_one)
        self.assertTrue(owner_field.null)
        self.assertEqual(
            owner_field.remote_field.related_name, "bonus_and_transfer_owner"
        )

    def test_bonus_and_transfer_to_client_foreignkey_field(self):
        client_field = BonusAndTransfer._meta.get_field("client")
        self.assertEqual(client_field.related_model, Client)
        self.assertTrue(client_field.many_to_one)
        self.assertTrue(client_field.null)
        self.assertEqual(
            client_field.remote_field.related_name, "bonus_and_transfer_client"
        )


class TestBonusAndTransfer(TestCase):
    def setUp(self) -> None:
        self.bonus_and_transfer_create = BonusAndTransfer.objects.create(
            sales_bonus=5000.50,
            profit_transfer=2000,
        )

    def test_bonus_and_transfer_instance_attrs(self):
        bonus_and_transfer = BonusAndTransferClass(
            sales_bonus=5000.50,
            profit_transfer=2000,
        )
        self.assertEqual(type(bonus_and_transfer.sales_bonus), float)
        self.assertEqual(type(bonus_and_transfer.profit_transfer), int)

    def test_bonus_and_transfer_serializer(self):
        bonus_and_transfer = self.bonus_and_transfer_create
        serializer = BonusAndTransferSerializer(bonus_and_transfer)
        data = serializer.data

        self.assertEqual(data["sales_bonus"], "5000.50")
        self.assertEqual(int(data["profit_transfer"]), 2000)
        self.assertIsNone(data["owner"])
        self.assertIsNone(data["client"])
