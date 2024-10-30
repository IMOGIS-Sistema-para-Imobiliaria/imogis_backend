from rest_framework import serializers
from bonus_and_transfer.models import BonusAndTransfer


class BonusAndTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusAndTransfer

        fields = [
            "sales_bonus",
            "profit_transfer",
            "owner",
            "client",
        ]
