from rest_framework import serializers
from bank_details.models import BankDetails


class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = [
            "bank",
            "account",
            "agency",
            "account_type",
            "owner",
            "client",
        ]
        extra_kwargs = {
            "owner": {"required": False},
            "client": {"required": False},
        }
