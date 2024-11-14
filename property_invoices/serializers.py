from rest_framework import serializers
from .models import PropertyInvoice


class PropertyInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyInvoice
        depth = 1
        fields = [
            "id",
            "month",
            "due_date",
            "rental_value",
            "status_invoice",
            "date_it_was_paid",
            "observations",
            "real_estate",
            "client",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "client": {
                "required": False,
                "allow_null": True,
            },
            "real_estate": {
                "required": False,
                "allow_null": True,
            },
        }
