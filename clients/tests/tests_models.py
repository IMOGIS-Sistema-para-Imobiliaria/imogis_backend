from django.test import TestCase
from clients.models import Client
from django.db import IntegrityError, models

from clients.serializers import ClientSerializer
from owners.models import Owner
from users.models import User


class ClientClass:
    def __init__(
        self,
        fullname: str,
        cpf: str,
        cnpj: str,
        telephone: str,
        address: str,
        occupation: str,
    ) -> None:
        self.fullname = fullname
        self.cpf = cpf
        self.cnpj = cnpj
        self.telephone = telephone
        self.address = address
        self.occupation = occupation


class TestClientModel(TestCase):
    def test_attrs(self):
        expected_attr_names = [
            "id",
            "fullname",
            "cpf",
            "cnpj",
            "telephone",
            "address",
            "occupation",
            "user",
            "owner",
        ]

        attr_names = []
        for attr in Client._meta.get_fields():
            if isinstance(attr, models.Field):
                attr_names.append(attr.name)

        for name in expected_attr_names:
            self.assertIn(name, attr_names)

        self.assertEqual(len(expected_attr_names), len(attr_names))

    def test_name_attr(self):
        fullname_field = Client._meta.get_field("fullname")
        self.assertIsInstance(fullname_field, models.CharField)
        self.assertEqual(fullname_field.max_length, 100)
        self.assertEqual(fullname_field.null, False)

        cpf_field = Client._meta.get_field("cpf")
        self.assertIsInstance(cpf_field, models.CharField)
        self.assertEqual(cpf_field.max_length, 11)
        self.assertEqual(cpf_field.blank, True)

        cnpj_field = Client._meta.get_field("cnpj")
        self.assertIsInstance(cnpj_field, models.CharField)
        self.assertEqual(cnpj_field.max_length, 14)
        self.assertEqual(cnpj_field.blank, True)

        telephone_field = Client._meta.get_field("telephone")
        self.assertIsInstance(telephone_field, models.CharField)
        self.assertEqual(telephone_field.max_length, 15)
        self.assertEqual(telephone_field.null, False)

        address_field = Client._meta.get_field("address")
        self.assertIsInstance(address_field, models.CharField)
        self.assertEqual(address_field.max_length, 255)
        self.assertEqual(address_field.null, False)

        occupation_field = Client._meta.get_field("occupation")
        self.assertIsInstance(occupation_field, models.CharField)
        self.assertEqual(occupation_field.max_length, 100)
        self.assertEqual(occupation_field.blank, True)
        self.assertEqual(occupation_field.null, True)

    def test_client_to_user_foreignkey_field(self):
        user_field = Client._meta.get_field("user")
        self.assertEqual(user_field.related_model, User)
        self.assertTrue(user_field.many_to_one)
        self.assertEqual(user_field.remote_field.related_name, "client_user")
        self.assertEqual(user_field.null, True)
        self.assertEqual(user_field.blank, True)

    def test_client_to_owner_foreignkey_field(self):
        owner_field = Client._meta.get_field("owner")
        self.assertEqual(owner_field.related_model, Owner)
        self.assertTrue(owner_field.many_to_one)
        self.assertEqual(owner_field.remote_field.related_name, "client_owner")
        self.assertEqual(owner_field.null, True)
        self.assertEqual(owner_field.blank, True)


class TestClient(TestCase):
    def setUp(self) -> None:
        self.client_create = Client.objects.create(
            fullname="testclient",
            cpf="12345678901",
            cnpj="12345678901234",
            telephone="+5511999999999",
            address="Test Street, 0",
            occupation="tester",
        )

    def test_owner_instance_attrs(self):
        client = ClientClass(
            "testclient",
            "12345678901",
            "12345678901234",
            "+5511999999999",
            "Test Street, 0",
            "tester",
        )
        self.assertEqual(type(client.fullname), str)
        self.assertEqual(type(client.cpf), str)
        self.assertEqual(type(client.cnpj), str)
        self.assertEqual(type(client.telephone), str)
        self.assertEqual(type(client.address), str)
        self.assertEqual(type(client.occupation), str)

    def test_unique_cpf(self):
        Client.objects.create(
            fullname="client1",
            cpf="11111111111",
            cnpj="22222222222222",
            telephone="+5511999999998",
            address="Another Street, 1",
            occupation="developer",
        )
        with self.assertRaises(IntegrityError):
            Client.objects.create(
                fullname="client1",
                cpf="11111111111",
                cnpj="33333333333333",
                telephone="+5511999999998",
                address="Another Street, 1",
                occupation="developer",
            )

    def test_unique_cnpj(self):
        Client.objects.create(
            fullname="client2",
            cpf="22222222222",
            cnpj="33333333333333",
            telephone="+5511999999997",
            address="Yet Another Street, 2",
            occupation="analyst",
        )
        with self.assertRaises(IntegrityError):
            Client.objects.create(
                fullname="client2",
                cpf="44444444444",
                cnpj="33333333333333",
                telephone="+5511999999997",
                address="Yet Another Street, 2",
                occupation="analyst",
            )

    def test_client_serializer(self):
        client = self.client_create
        serializer = ClientSerializer(client)
        data = serializer.data

        self.assertEqual(data["fullname"], "testclient")
        self.assertEqual(data["cpf"], "12345678901")
        self.assertEqual(data["cnpj"], "12345678901234")
        self.assertEqual(data["telephone"], "+5511999999999")
        self.assertEqual(data["address"], "Test Street, 0")
        self.assertEqual(data["occupation"], "tester")
