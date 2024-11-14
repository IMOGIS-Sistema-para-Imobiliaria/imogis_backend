from django.test import TestCase
from django.db import models

from clients.models import Client
from owners.models import Owner
from real_estate.models import ENUM_Type_Of_Housing, RealEstate
from real_estate.serializers import RealEstateSerializer


class RealEstateClass:
    def __init__(
        self,
        type_of_housing: str,
        address: str,
        owner_name: str,
        client_name: str,
        about_the_property: str,
        rental_value: int,
        tenant_present: bool,
        readjustment_date: str,
    ) -> None:
        self.type_of_housing = type_of_housing
        self.address = address
        self.owner_name = owner_name
        self.client_name = client_name
        self.about_the_property = about_the_property
        self.rental_value = rental_value
        self.tenant_present = tenant_present
        self.readjustment_date = readjustment_date


class TestRealEstateModel(TestCase):
    def test_attrs(self):
        expected_attr_names = [
            "id",
            "type_of_housing",
            "address",
            "owner_name",
            "client_name",
            "about_the_property",
            "rental_value",
            "tenant_present",
            "readjustment_date",
            "client",
            "owner",
        ]

        attr_names = []
        for attr in RealEstate._meta.get_fields():
            if isinstance(attr, models.Field):
                attr_names.append(attr.name)

        for name in expected_attr_names:
            self.assertIn(name, attr_names)

        self.assertEqual(len(expected_attr_names), len(attr_names))

    def test_type_of_housing_attr(self):
        type_of_housing_field = RealEstate._meta.get_field("type_of_housing")
        self.assertIsInstance(type_of_housing_field, models.CharField)
        self.assertEqual(type_of_housing_field.max_length, 7)
        self.assertEqual(
            type_of_housing_field.choices, ENUM_Type_Of_Housing.choices
        )
        self.assertEqual(type_of_housing_field.null, False)

    def test_address_attr(self):
        address_field = RealEstate._meta.get_field("address")
        self.assertIsInstance(address_field, models.CharField)
        self.assertEqual(address_field.max_length, 255)
        self.assertEqual(address_field.null, False)

    def test_rental_value_attr(self):
        rental_value_field = RealEstate._meta.get_field("rental_value")
        self.assertIsInstance(rental_value_field, models.PositiveIntegerField)
        self.assertEqual(rental_value_field.null, False)

    def test_tenant_present_attr(self):
        tenant_present_field = RealEstate._meta.get_field("tenant_present")
        self.assertIsInstance(tenant_present_field, models.BooleanField)
        self.assertEqual(tenant_present_field.null, False)

    def test_client_foreignkey_field(self):
        client_field = RealEstate._meta.get_field("client")
        self.assertEqual(client_field.related_model, Client)
        self.assertTrue(client_field.one_to_one)
        self.assertEqual(client_field.null, True)
        self.assertEqual(client_field.blank, True)
        self.assertEqual(client_field.default, None)
        self.assertEqual(
            client_field.remote_field.related_name, "real_estate_client"
        )

    def test_owner_foreignkey_field(self):
        owner_field = RealEstate._meta.get_field("owner")
        self.assertEqual(owner_field.related_model, Owner)
        self.assertTrue(owner_field.many_to_one)
        self.assertEqual(owner_field.null, True)
        self.assertEqual(owner_field.blank, True)
        self.assertEqual(
            owner_field.remote_field.related_name, "real_estate_owner"
        )


class TestRealEstate(TestCase):
    def setUp(self) -> None:
        self.real_estate_instance = RealEstate.objects.create(
            type_of_housing="Aluguel",
            address="Rua Exemplo, 123",
            owner_name="Proprietário XYZ",
            client_name="Cliente ABC",
            about_the_property="Apartamento com vista para o mar.",
            rental_value=2000,
            tenant_present=True,
            readjustment_date="2024-01-01T00:00:00Z",
        )

    def test_real_estate_instance_attrs(self):
        real_estate = RealEstateClass(
            "Aluguel",
            "Rua Exemplo, 123",
            "Proprietário XYZ",
            "Cliente ABC",
            "Apartamento com vista para o mar.",
            2000,
            True,
            "2024-01-01T00:00:00Z",
        )
        self.assertEqual(type(real_estate.type_of_housing), str)
        self.assertEqual(type(real_estate.address), str)
        self.assertEqual(type(real_estate.owner_name), str)
        self.assertEqual(type(real_estate.client_name), str)
        self.assertEqual(type(real_estate.about_the_property), str)
        self.assertEqual(type(real_estate.rental_value), int)
        self.assertEqual(type(real_estate.tenant_present), bool)
        self.assertEqual(type(real_estate.readjustment_date), str)

    def test_real_estate_serializer(self):
        real_estate = self.real_estate_instance
        serializer = RealEstateSerializer(real_estate)
        data = serializer.data

        self.assertEqual(data["type_of_housing"], "Aluguel")
        self.assertEqual(data["address"], "Rua Exemplo, 123")
        self.assertEqual(data["owner_name"], "Proprietário XYZ")
        self.assertEqual(data["client_name"], "Cliente ABC")
        self.assertEqual(
            data["about_the_property"], "Apartamento com vista para o mar."
        )
        self.assertEqual(data["rental_value"], 2000)
        self.assertEqual(data["tenant_present"], True)
        self.assertEqual(data["readjustment_date"], "2024-01-01T00:00:00Z")
