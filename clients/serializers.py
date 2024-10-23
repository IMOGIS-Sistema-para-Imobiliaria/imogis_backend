from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "fullname",
            "cpf",
            "telephone",
            "address",
            "occupation",
            "owner_name",
            "user",
            "real_estate_id",
            "contract_id",
        ]
