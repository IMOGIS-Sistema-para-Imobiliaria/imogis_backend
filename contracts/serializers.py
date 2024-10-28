from rest_framework import serializers
from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = [
            "id",
            "contract_belongs_to",
            "type_of_contract",
            "status",
            "contract_duration",
            "start_of_contract",
            "end_of_contract",
            "rental_value",
            "due_date",
            "client_id",
            "owner_id",
            "real_estate_id",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }
