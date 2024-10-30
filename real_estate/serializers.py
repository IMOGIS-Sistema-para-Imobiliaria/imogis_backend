from rest_framework import serializers
from .models import RealEstate


class RealEstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstate
        fields = [
            "id",
            "type_of_housing",
            "address",
            "owner_name",
            "client_name",
            "about_the_property",
            "rental_value",
            "tenant_present",
            "readjustment_date",
            "contract",
            "client",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
        }
