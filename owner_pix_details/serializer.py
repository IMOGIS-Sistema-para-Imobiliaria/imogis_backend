from rest_framework import serializers
from .models import OwnerPixDetails


class OwnerPixDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerPixDetails
        fields = ["pix_key", "pix_type"]
