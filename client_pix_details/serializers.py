from rest_framework import serializers
from .models import ClientPixDetails


class ClientPixDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientPixDetails
        fields = ["pix_key", "pix_type"]
