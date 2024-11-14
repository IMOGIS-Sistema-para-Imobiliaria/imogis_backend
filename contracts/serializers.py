from rest_framework import serializers
from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        depth = 1
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
            "client",
            "owner",
            "real_estate",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "client": {
                "required": False,
                "allow_null": True,
            },
            "owner": {
                "required": False,
                "allow_null": True,
            },
            "real_estate": {
                "required": False,
                "allow_null": True,
            },
        }
