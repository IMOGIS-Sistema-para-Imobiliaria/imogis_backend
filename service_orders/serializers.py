from rest_framework import serializers
from .models import ServiceOrder


class ServiceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        fields = [
            "id",
            "service_category",
            "service_provided",
            "price",
            "payment_status",
            "date_paid",
            "start_date",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "owner": {"read_only": True},
        }
