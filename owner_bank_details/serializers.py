from rest_framework import serializers
from .models import OwnerBankDetails


class OwnerBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerBankDetails
        fields = ["bank", "account", "agency"]
