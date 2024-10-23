from rest_framework import serializers
from .models import Client
from rest_framework.validators import UniqueValidator


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "fullname",
            "cpf",
            "cnpj",
            "telephone",
            "address",
            "occupation",
            "owner_name",
            "real_estate_id",
            "contract_id",
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
            "real_estate_id": {"required": False, "allow_null": True},
            "contract_id": {"required": False, "allow_null": True},
        }
