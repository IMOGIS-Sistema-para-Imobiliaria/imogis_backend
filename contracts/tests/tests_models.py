from django.test import TestCase
from django.db import models
from clients.models import Client
from contracts.models import (
    Contract,
    ENUM_Status_Of_Contract,
    ENUM_Type_Of_Contract,
)
from contracts.serializers import ContractSerializer
from owners.models import Owner
from real_estate.models import RealEstate


class ContractClass:
    def __init__(
        self,
        contract_belongs_to: str,
        type_of_contract: str,
        status: str,
        contract_duration: int,
        start_of_contract: str,
        end_of_contract: str,
        rental_value: int,
        due_date: int,
    ) -> None:
        self.contract_belongs_to = contract_belongs_to
        self.type_of_contract = type_of_contract
        self.status = status
        self.contract_duration = contract_duration
        self.start_of_contract = start_of_contract
        self.end_of_contract = end_of_contract
        self.rental_value = rental_value
        self.due_date = due_date


class TestClientModel(TestCase):
    def test_attrs(self):
        expected_attr_names = [
            "id",
            "contract_belongs_to",
            "type_of_contract",
            "status",
            "contract_duration",
            "start_of_contract",
            "end_of_contract",
            "rental_value",
            "due_date",
            "client",
            "owner",
            "real_estate",
        ]

        attr_names = []
        for attr in Contract._meta.get_fields():
            if isinstance(attr, models.Field):
                attr_names.append(attr.name)

        for name in expected_attr_names:
            self.assertIn(name, attr_names)

        self.assertEqual(len(expected_attr_names), len(attr_names))

    def test_name_attr(self):
        contract_belongs_to_field = Contract._meta.get_field(
            "contract_belongs_to"
        )
        self.assertIsInstance(contract_belongs_to_field, models.CharField)
        self.assertEqual(contract_belongs_to_field.max_length, 100)
        self.assertEqual(contract_belongs_to_field.null, False)
        self.assertEqual(contract_belongs_to_field.blank, False)

        type_of_contract_field = Contract._meta.get_field("type_of_contract")
        self.assertIsInstance(type_of_contract_field, models.CharField)
        self.assertEqual(type_of_contract_field.max_length, 13)
        self.assertEqual(
            type_of_contract_field.choices, ENUM_Type_Of_Contract.choices
        )
        self.assertEqual(
            type_of_contract_field.default, ENUM_Type_Of_Contract.NAO_INFORMADO
        )
        self.assertEqual(type_of_contract_field.null, False)

        status_field = Contract._meta.get_field("status")
        self.assertIsInstance(status_field, models.CharField)
        self.assertEqual(status_field.max_length, 8)
        self.assertEqual(status_field.choices, ENUM_Status_Of_Contract.choices)
        self.assertEqual(
            status_field.default, ENUM_Status_Of_Contract.PENDENTE
        )
        self.assertEqual(status_field.null, False)

        contract_duration_field = Contract._meta.get_field("contract_duration")
        self.assertIsInstance(
            contract_duration_field, models.PositiveIntegerField
        )
        self.assertEqual(contract_duration_field.null, False)

        start_of_contract_field = Contract._meta.get_field("start_of_contract")
        self.assertIsInstance(start_of_contract_field, models.DateTimeField)
        self.assertEqual(start_of_contract_field.null, False)

        end_of_contract_field = Contract._meta.get_field("end_of_contract")
        self.assertIsInstance(end_of_contract_field, models.DateTimeField)
        self.assertEqual(end_of_contract_field.null, False)

        rental_value_field = Contract._meta.get_field("rental_value")
        self.assertIsInstance(rental_value_field, models.PositiveIntegerField)
        self.assertEqual(rental_value_field.null, False)

        due_date_field = Contract._meta.get_field("due_date")
        self.assertIsInstance(due_date_field, models.PositiveIntegerField)
        self.assertEqual(due_date_field.null, False)

    def test_contract_to_client_one_to_one_field(self):
        client_field = Contract._meta.get_field("client")
        self.assertEqual(client_field.related_model, Client)
        self.assertTrue(client_field.one_to_one)
        self.assertEqual(
            client_field.remote_field.related_name, "contract_client"
        )
        self.assertEqual(client_field.null, True)
        self.assertEqual(client_field.blank, True)
        self.assertEqual(client_field.default, None)

    def test_contract_to_owner_one_to_one_field(self):
        owner_field = Contract._meta.get_field("owner")
        self.assertEqual(owner_field.related_model, Owner)
        self.assertTrue(owner_field.one_to_one)
        self.assertEqual(
            owner_field.remote_field.related_name, "contract_owner"
        )
        self.assertEqual(owner_field.null, True)
        self.assertEqual(owner_field.blank, True)
        self.assertEqual(owner_field.default, None)

    def test_contract_to_real_estate_one_to_one_field(self):
        real_estate_field = Contract._meta.get_field("real_estate")
        self.assertEqual(real_estate_field.related_model, RealEstate)
        self.assertTrue(real_estate_field.one_to_one)
        self.assertEqual(
            real_estate_field.remote_field.related_name, "contract_real_estate"
        )
        self.assertEqual(real_estate_field.null, True)
        self.assertEqual(real_estate_field.blank, True)
        self.assertEqual(real_estate_field.default, None)


class TestContract(TestCase):
    def setUp(self) -> None:
        self.contract_create = Contract.objects.create(
            contract_belongs_to="Cliente XYZ",
            type_of_contract="Aluguel",
            status="Pendente",
            contract_duration=12,
            start_of_contract="2024-01-01T00:00:00Z",
            end_of_contract="2025-01-01T00:00:00Z",
            rental_value=1500,
            due_date=5,
        )

    def test_contract_instance_attrs(self):
        contract = ContractClass(
            "Cliente XYZ",
            "Aluguel",
            "Pendente",
            12,
            "2024-01-01T00:00:00Z",
            "2025-01-01T00:00:00Z",
            1500,
            5,
        )
        self.assertEqual(type(contract.contract_belongs_to), str)
        self.assertEqual(type(contract.type_of_contract), str)
        self.assertEqual(type(contract.status), str)
        self.assertEqual(type(contract.contract_duration), int)
        self.assertEqual(type(contract.start_of_contract), str)
        self.assertEqual(type(contract.end_of_contract), str)
        self.assertEqual(type(contract.rental_value), int)
        self.assertEqual(type(contract.due_date), int)

    def test_contract_serializer(self):
        contract = self.contract_create
        serializer = ContractSerializer(contract)
        data = serializer.data

        self.assertEqual(data["contract_belongs_to"], "Cliente XYZ")
        self.assertEqual(data["type_of_contract"], "Aluguel")
        self.assertEqual(data["status"], "Pendente")
        self.assertEqual(data["contract_duration"], 12)
        self.assertEqual(data["start_of_contract"], "2024-01-01T00:00:00Z")
        self.assertEqual(data["end_of_contract"], "2025-01-01T00:00:00Z")
        self.assertEqual(data["rental_value"], 1500)
        self.assertEqual(data["due_date"], 5)
