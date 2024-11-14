from django.test import TestCase
from django.db import IntegrityError, models
from owners.models import ENUM_TYPE_OF_SALE, Owner
from owners.serializers import OwnerSerializer
from users.models import User


class OwnerClass:
    def __init__(
        self,
        fullname: str,
        cpf: str,
        cnpj: str,
        telephone: str,
        address: str,
        occupation: str,
        type_of_sale: str,
    ) -> None:
        self.fullname = fullname
        self.cpf = cpf
        self.cnpj = cnpj
        self.telephone = telephone
        self.address = address
        self.occupation = occupation
        self.type_of_sale = type_of_sale


class TestOwnerModel(TestCase):
    def test_attrs(self):
        expected_attr_names = [
            "id",
            "fullname",
            "cpf",
            "cnpj",
            "telephone",
            "address",
            "occupation",
            "type_of_sale",
            "user",
        ]

        attr_names = []
        for attr in Owner._meta.get_fields():
            if isinstance(attr, models.Field):
                attr_names.append(attr.name)

        for name in expected_attr_names:
            self.assertIn(name, attr_names)

        self.assertEqual(len(expected_attr_names), len(attr_names))

    def test_name_attr(self):
        fullname_field = Owner._meta.get_field("fullname")
        self.assertIsInstance(fullname_field, models.CharField)
        self.assertEqual(fullname_field.max_length, 100)
        self.assertEqual(fullname_field.null, False)

        cpf_field = Owner._meta.get_field("cpf")
        self.assertIsInstance(cpf_field, models.CharField)
        self.assertEqual(cpf_field.max_length, 11)
        self.assertEqual(cpf_field.blank, True)

        cnpj_field = Owner._meta.get_field("cnpj")
        self.assertIsInstance(cnpj_field, models.CharField)
        self.assertEqual(cnpj_field.max_length, 14)
        self.assertEqual(cnpj_field.blank, True)

        telephone_field = Owner._meta.get_field("telephone")
        self.assertIsInstance(telephone_field, models.CharField)
        self.assertEqual(telephone_field.max_length, 15)
        self.assertEqual(telephone_field.null, False)

        address_field = Owner._meta.get_field("address")
        self.assertIsInstance(address_field, models.CharField)
        self.assertEqual(address_field.max_length, 255)
        self.assertEqual(address_field.null, False)

        occupation_field = Owner._meta.get_field("occupation")
        self.assertIsInstance(occupation_field, models.CharField)
        self.assertEqual(occupation_field.max_length, 100)
        self.assertEqual(occupation_field.null, True)
        self.assertEqual(occupation_field.blank, True)

        type_of_sale_field = Owner._meta.get_field("type_of_sale")
        self.assertIsInstance(type_of_sale_field, models.CharField)
        self.assertEqual(type_of_sale_field.max_length, 50)
        self.assertEqual(type_of_sale_field.null, True)
        self.assertEqual(type_of_sale_field.choices, ENUM_TYPE_OF_SALE.choices)

    def test_owner_to_user_foreignkey_field(self):
        user_field = Owner._meta.get_field("user")
        self.assertEqual(user_field.related_model, User)
        self.assertTrue(user_field.many_to_one)
        self.assertEqual(user_field.remote_field.related_name, "owner_user")
        self.assertEqual(user_field.null, True)
        self.assertEqual(user_field.blank, True)


class TestOwner(TestCase):
    def setUp(self) -> None:
        self.owner_create = Owner.objects.create(
            fullname="testowner",
            cpf="12345678901",
            cnpj="12345678901234",
            telephone="+5511999999999",
            address="Test Address, 123",
            occupation="owner occupation",
            type_of_sale="Aluguel",
        )

    def test_owner_instance_attrs(self):
        owner = OwnerClass(
            "testowner",
            "98765432109",
            "98765432109876",
            "+5511987654321",
            "Another Test Address, 456",
            "owner occupation",
            "Aluguel",
        )
        self.assertEqual(type(owner.fullname), str)
        self.assertEqual(type(owner.cpf), str)
        self.assertEqual(type(owner.cnpj), str)
        self.assertEqual(type(owner.telephone), str)
        self.assertEqual(type(owner.address), str)
        self.assertEqual(type(owner.occupation), str)
        self.assertEqual(type(owner.type_of_sale), str)

    def test_unique_cpf(self):
        Owner.objects.create(
            fullname="testowner",
            cpf="11111111111",
            cnpj="22222222222222",
            telephone="+5511987654321",
            address="Test Address, 789",
            occupation="owner occupation",
            type_of_sale="Aluguel",
        )
        with self.assertRaises(IntegrityError):
            Owner.objects.create(
                fullname="testowner",
                cpf="11111111111",
                cnpj="33333333333333",
                telephone="+5511987654321",
                address="Test Address, 789",
                occupation="owner occupation",
                type_of_sale="Aluguel",
            )

    def test_unique_cnpj(self):
        Owner.objects.create(
            fullname="testowner",
            cpf="33333333333",
            cnpj="44444444444444",
            telephone="+5511987654321",
            address="Another Test Address, 789",
            occupation="owner occupation",
            type_of_sale="Aluguel",
        )
        with self.assertRaises(IntegrityError):
            Owner.objects.create(
                fullname="testowner",
                cpf="55555555555",
                cnpj="44444444444444",
                telephone="+5511987654321",
                address="Another Test Address, 789",
                occupation="owner occupation",
                type_of_sale="Aluguel",
            )

    def test_owner_serializer(self):
        owner = self.owner_create

        serializer = OwnerSerializer(owner)
        data = serializer.data

        self.assertEqual(data["fullname"], "testowner")
        self.assertEqual(data["cpf"], "12345678901")
        self.assertEqual(data["cnpj"], "12345678901234")
        self.assertEqual(data["telephone"], "+5511999999999")
        self.assertEqual(data["address"], "Test Address, 123")
        self.assertEqual(data["occupation"], "owner occupation")
        self.assertEqual(data["type_of_sale"], "Aluguel")
