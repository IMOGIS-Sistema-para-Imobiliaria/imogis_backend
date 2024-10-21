from rest_framework import serializers
from .models import OwnerPaymentMethod


class OwnerPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerPaymentMethod
        fields = "__all__"
        extra_kwargs = {
            "owner_id": {"read_only": True},
        }

    def update(self, instance: OwnerPaymentMethod, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
