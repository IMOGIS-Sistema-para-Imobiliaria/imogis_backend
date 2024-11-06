from rest_framework import serializers
from bonus_and_transfer.models import BonusAndTransfer


class BonusAndTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusAndTransfer
        depth = 1
        fields = [
            "id",
            "sales_bonus",
            "profit_transfer",
            "owner",
            "client",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "owner": {
                "required": False,
                "allow_null": True,
            },
            "client": {
                "required": False,
                "allow_null": True,
            },
        }
