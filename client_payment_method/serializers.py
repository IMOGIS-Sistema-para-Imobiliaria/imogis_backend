from rest_framework import serializers
from client_bank_details.models import ClientBankDetails
from client_bank_details.serializers import ClientBankDetailsSerializer
from client_pix_details.models import ClientPixDetails
from client_pix_details.serializers import ClientPixDetailsSerializer
from .models import ClientPaymentMethod


class ClientPaymentMethodSerializer(serializers.ModelSerializer):
    bank_details = ClientBankDetailsSerializer(many=True)
    pix_details = ClientPixDetailsSerializer(many=True)

    class Meta:
        model = ClientPaymentMethod
        fields = [
            "id",
            "sales_bonus",
            "profit_transfer",
            "client",
            "bank_details",
            "pix_details",
        ]
        extra_kwargs = {
            "client": {"read_only": True},
        }

    def create(
        self, validated_data: dict[str, list[dict[str, str]]]
    ) -> ClientPaymentMethod:
        bank_details_data: list[dict[str, str]] = validated_data.pop(
            "bank_details"
        )
        pix_details_data: list[dict[str, str]] = validated_data.pop(
            "pix_details"
        )

        instance: ClientPaymentMethod = ClientPaymentMethod.objects.create(
            **validated_data
        )

        for bank_detail in bank_details_data:
            ClientBankDetails.objects.create(
                client_payment_method=instance, **bank_detail
            )

        for pix_detail in pix_details_data:
            ClientPixDetails.objects.create(
                client_payment_method=instance, **pix_detail
            )

        return instance

    def update(
        self, instance: ClientPaymentMethod, validated_data: dict[str, str]
    ) -> ClientPaymentMethod:
        instance.sales_bonus = validated_data.get(
            "sales_bonus",
            instance.sales_bonus,
        )

        instance.profit_transfer = validated_data.get(
            "profit_transfer",
            instance.profit_transfer,
        )

        instance.save()
        return instance
