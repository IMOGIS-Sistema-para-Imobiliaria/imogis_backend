from rest_framework import serializers
from .models import PixDetails


class PixDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PixDetails
        fields = [
            "pix_key",
            "pix_type",
            "owner",
            "client",
        ]
        extra_kwargs = {
            "owner": {"required": False},
            "client": {"required": False},
        }
