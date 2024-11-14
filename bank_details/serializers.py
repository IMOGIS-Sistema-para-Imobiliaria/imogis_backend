from rest_framework import serializers
from bank_details.models import BankDetails


class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        depth = 1
        fields = [
            "id",
            "bank",
            "account",
            "agency",
            "account_type",
            "owner",
            "client",
        ]
        extra_kwargs = {
            "owner": {
                "required": False,
                "allow_null": True,
            },
            "client": {
                "required": False,
                "allow_null": True,
            },
        }
