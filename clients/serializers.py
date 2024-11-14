from rest_framework import serializers
from .models import Client
from rest_framework.validators import UniqueValidator


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        depth = 1
        fields = [
            "id",
            "fullname",
            "cpf",
            "cnpj",
            "telephone",
            "address",
            "occupation",
            "owner",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "cpf": {
                "validators": [
                    UniqueValidator(
                        queryset=Client.objects.all(),
                        message="A client with this CPF already exists.",
                    )
                ]
            },
            "cnpj": {
                "validators": [
                    UniqueValidator(
                        queryset=Client.objects.all(),
                        message="A client with this CNPJ already exists.",
                    )
                ]
            },
            "user": {
                "required": False,
                "allow_null": True,
            },
            "owner": {
                "required": False,
                "allow_null": True,
            },
        }
