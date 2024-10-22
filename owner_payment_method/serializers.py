from rest_framework import serializers

from owner_bank_details.models import OwnerBankDetails
from owner_bank_details.serializers import OwnerBankDetailsSerializer
from owner_pix_details.models import OwnerPixDetails
from owner_pix_details.serializer import OwnerPixDetailsSerializer
from .models import OwnerPaymentMethod
from rest_framework.views import Response, status


class OwnerPaymentMethodSerializer(serializers.ModelSerializer):
    bank_details = OwnerBankDetailsSerializer(many=True)
    pix_details = OwnerPixDetailsSerializer(many=True)

    class Meta:
        model = OwnerPaymentMethod
        fields = [
            "id",
            "sales_bonus",
            "profit_transfer",
            "owner",
            "bank_details",
            "pix_details",
        ]
        extra_kwargs = {
            "owner": {"read_only": True},
        }

    def create(self, validated_data):
        bank_details_data = validated_data.pop("bank_details")
        pix_details_data = validated_data.pop("pix_details")

        owner_payment_method = (
            self.instance
            or OwnerPaymentMethod.objects.create(**validated_data)
        )

        if not owner_payment_method:
            return Response(
                {"message": "Payment method already exists."},
                status=status.HTTP_200_OK,
            )

        for bank_detail in bank_details_data:
            OwnerBankDetails.objects.create(
                owner_payment_method=owner_payment_method, **bank_detail
            )

        for pix_detail in pix_details_data:
            OwnerPixDetails.objects.create(
                owner_payment_method=owner_payment_method, **pix_detail
            )

        return owner_payment_method

    def update(self, instance: OwnerPaymentMethod, validated_data: dict):
        for key, value in validated_data.items():
            if key not in ["bank_details", "pix_details"]:
                setattr(instance, key, value)
        instance.save()

        bank_details_data = validated_data.pop("bank_details", [])
        existing_bank_details_ids = {
            bd.id for bd in instance.bank_details.all()
        }

        for bank_detail in bank_details_data:
            existing_bank_detail = OwnerBankDetails.objects.filter(
                owner_payment_method=instance,
                bank=bank_detail.get("bank"),
                account=bank_detail.get("account"),
                agency=bank_detail.get("agency"),
            ).first()

            if existing_bank_detail:
                for key, value in bank_detail.items():
                    setattr(existing_bank_detail, key, value)
                existing_bank_detail.save()
                existing_bank_details_ids.discard(existing_bank_detail.id)

            else:
                OwnerBankDetails.objects.create(
                    owner_payment_method=instance, **bank_detail
                )

        for bd_id in existing_bank_details_ids:
            OwnerBankDetails.objects.filter(id=bd_id).delete()

        pix_details_data = validated_data.pop("pix_details", [])
        existing_pix_details_ids = {pd.id for pd in instance.pix_details.all()}

        for pix_detail in pix_details_data:
            existing_pix_detail = OwnerPixDetails.objects.filter(
                owner_payment_method=instance,
                pix_key=pix_detail.get("pix_key"),
            ).first()

            if existing_pix_detail:
                for key, value in pix_detail.items():
                    setattr(existing_pix_detail, key, value)
                existing_pix_detail.save()
                existing_pix_details_ids.discard(existing_pix_detail.id)
            else:
                OwnerPixDetails.objects.create(
                    owner_payment_method=instance, **pix_detail
                )

        for pd_id in existing_pix_details_ids:
            OwnerPixDetails.objects.filter(id=pd_id).delete()

        return instance
