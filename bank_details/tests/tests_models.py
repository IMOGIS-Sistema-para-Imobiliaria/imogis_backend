from django.test import TestCase
from django.db import models
from clients.models import Client
from owners.models import Owner
from bank_details.models import ENUM_ACCOUNT_TYPE, ENUM_BANKS, BankDetails
from bank_details.serializers import BankDetailsSerializer


class BankDetailsClass:
    def __init__(
        self,
        bank: str,
        account: str,
        agency: str,
        account_type: str,
    ) -> None:
        self.bank = bank
        self.account = account
        self.agency = agency
        self.account_type = account_type


class TestBankDetailsModel(TestCase):
    def test_attrs(self):
        expected_attr_names = [
            "id",
            "bank",
            "account",
            "agency",
            "account_type",
            "owner",
            "client",
        ]

        attr_names = []
        for attr in BankDetails._meta.get_fields():
            if isinstance(attr, models.Field):
                attr_names.append(attr.name)

        for name in expected_attr_names:
            self.assertIn(name, attr_names)

        self.assertEqual(len(expected_attr_names), len(attr_names))

    def test_name_attr(self):
        bank_field = BankDetails._meta.get_field("bank")
        self.assertIsInstance(bank_field, models.CharField)
        self.assertEqual(bank_field.max_length, 25)
        self.assertEqual(bank_field.choices, ENUM_BANKS.choices)
        self.assertEqual(bank_field.null, False)

        account_field = BankDetails._meta.get_field("account")
        self.assertIsInstance(account_field, models.CharField)
        self.assertEqual(account_field.max_length, 20)
        self.assertEqual(account_field.unique, True)
        self.assertEqual(account_field.null, False)

        agency_field = BankDetails._meta.get_field("agency")
        self.assertIsInstance(agency_field, models.CharField)
        self.assertEqual(agency_field.max_length, 6)
        self.assertEqual(agency_field.null, False)

        account_type_field = BankDetails._meta.get_field("account_type")
        self.assertIsInstance(account_type_field, models.CharField)
        self.assertEqual(account_type_field.max_length, 255)
        self.assertEqual(account_type_field.choices, ENUM_ACCOUNT_TYPE.choices)
        self.assertEqual(account_type_field.null, False)

    def test_bank_details_to_owner_foreignkey_field(self):
        owner_field = BankDetails._meta.get_field("owner")
        self.assertEqual(owner_field.related_model, Owner)
        self.assertTrue(owner_field.many_to_one)
        self.assertTrue(owner_field.null)
        self.assertEqual(
            owner_field.remote_field.related_name, "bank_details_owner"
        )

    def test_bank_details_to_client_foreignkey_field(self):
        client_field = BankDetails._meta.get_field("client")
        self.assertEqual(client_field.related_model, Client)
        self.assertTrue(client_field.many_to_one)
        self.assertTrue(client_field.null)
        self.assertEqual(
            client_field.remote_field.related_name, "bank_details_client"
        )


class TestBankDetails(TestCase):
    def setUp(self) -> None:
        self.bank_details_create = BankDetails.objects.create(
            bank="Banco do Brasil",
            account="1234567890",
            agency="123456",
            account_type="Conta Corrente",
        )

    def test_bank_details_instance_attrs(self):
        bank_details = BankDetailsClass(
            bank="Banco do Brasil",
            account="1234567890",
            agency="123456",
            account_type="Conta Corrente",
        )
        self.assertEqual(type(bank_details.bank), str)
        self.assertEqual(type(bank_details.account), str)
        self.assertEqual(type(bank_details.agency), str)
        self.assertEqual(type(bank_details.account_type), str)

    def test_bank_details_serializer(self):
        bank_details = self.bank_details_create
        serializer = BankDetailsSerializer(bank_details)
        data = serializer.data

        self.assertEqual(data["bank"], "Banco do Brasil")
        self.assertEqual(data["account"], "1234567890")
        self.assertEqual(data["agency"], "123456")
        self.assertEqual(data["account_type"], "Conta Corrente")
        self.assertIsNone(data["owner"])
        self.assertIsNone(data["client"])
