from rest_framework import serializers
from .models import ClientBankDetails


class ClientBankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientBankDetails
        fields = ["bank", "account", "agency", "account_type"]
