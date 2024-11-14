from rest_framework import serializers
from .models import ServiceOrder


class ServiceOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        depth = 1
        fields = [
            "id",
            "service_category",
            "service_provided",
            "price",
            "payment_status",
            "date_paid",
            "start_date",
            "owner",
            "real_estate",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "owner": {
                "required": False,
                "allow_null": True,
            },
            "real_estate": {
                "required": False,
                "allow_null": True,
            },
        }
