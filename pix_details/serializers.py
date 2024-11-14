from rest_framework import serializers
from .models import PixDetails


class PixDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PixDetails
        depth = 1
        fields = [
            "id",
            "pix_key",
            "pix_type",
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
