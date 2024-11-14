from django.test import TestCase
from django.db import models
from clients.models import Client
from owners.models import Owner
from pix_details.models import ENUM_PIX_TYPE_CLIENT, PixDetails
from pix_details.serializers import PixDetailsSerializer


class PixDetailsClass:
    def __init__(self, pix_key: str, pix_type: str) -> None:
        self.pix_key = pix_key
        self.pix_type = pix_type


class TestPixDetailsModel(TestCase):
    def test_attrs(self):
        expected_attr_names = [
            "id",
            "pix_key",
            "pix_type",
            "owner",
            "client",
        ]

        attr_names = []
        for attr in PixDetails._meta.get_fields():
            if isinstance(attr, models.Field):
                attr_names.append(attr.name)

        for name in expected_attr_names:
            self.assertIn(name, attr_names)

        self.assertEqual(len(expected_attr_names), len(attr_names))

    def test_name_attr(self):
        pix_key_field = PixDetails._meta.get_field("pix_key")
        self.assertIsInstance(pix_key_field, models.CharField)
        self.assertEqual(pix_key_field.max_length, 36)
        self.assertEqual(pix_key_field.null, True)
        self.assertEqual(pix_key_field.blank, True)
        self.assertEqual(pix_key_field.unique, True)

        pix_type_field = PixDetails._meta.get_field("pix_type")
        self.assertIsInstance(pix_type_field, models.CharField)
        self.assertEqual(pix_type_field.max_length, 15)
        self.assertEqual(pix_type_field.choices, ENUM_PIX_TYPE_CLIENT.choices)
        self.assertEqual(
            pix_type_field.default, ENUM_PIX_TYPE_CLIENT.NAO_POSSUI_PIX
        )
        self.assertEqual(pix_type_field.null, False)

    def test_pix_to_owner_foreignkey_field(self):
        owner_field = PixDetails._meta.get_field("owner")
        self.assertEqual(owner_field.related_model, Owner)
        self.assertTrue(owner_field.many_to_one)
        self.assertEqual(
            owner_field.remote_field.related_name, "pix_details_owner"
        )
        self.assertEqual(owner_field.null, True)
        self.assertEqual(owner_field.blank, True)
        self.assertEqual(owner_field.default, None)

    def test_pix_to_client_foreignkey_field(self):
        client_field = PixDetails._meta.get_field("client")
        self.assertEqual(client_field.related_model, Client)
        self.assertTrue(client_field.many_to_one)
        self.assertEqual(
            client_field.remote_field.related_name, "pix_details_client"
        )
        self.assertEqual(client_field.null, True)
        self.assertEqual(client_field.blank, True)
        self.assertEqual(client_field.default, None)


class TestPixDetails(TestCase):
    def setUp(self) -> None:
        self.pix_create = PixDetails.objects.create(
            pix_key="123e4567-e89b-12d3-a456-426614174000",
            pix_type=ENUM_PIX_TYPE_CLIENT.CPF,
        )

    def test_pix_instance_attrs(self):
        pix = PixDetailsClass(
            "123e4567-e89b-12d3-a456-426614174000",
            "Não Possui Pix",
        )
        self.assertEqual(type(pix.pix_key), str)
        self.assertEqual(type(pix.pix_type), str)

    def test_pix_serializer(self):
        pix = self.pix_create
        serializer = PixDetailsSerializer(pix)
        data = serializer.data

        self.assertEqual(
            data["pix_key"], "123e4567-e89b-12d3-a456-426614174000"
        )
        self.assertEqual(data["pix_type"], ENUM_PIX_TYPE_CLIENT.CPF)
