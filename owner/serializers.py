from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Owner


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = [
            "id",
            "fullname",
            "cpf",
            "cnpj",
            "telephone",
            "address",
            "occupation",
            "type_of_sale",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "cpf": {
                "validators": [
                    UniqueValidator(
                        queryset=Owner.objects.all(),
                        message="An owner with this CPF already exists.",
                    )
                ]
            },
            "cnpj": {
                "validators": [
                    UniqueValidator(
                        queryset=Owner.objects.all(),
                        message="An owner with this CNPJ already exists.",
                    )
                ]
            },
        }

    def update(self, instance: Owner, validated_data: dict):
        for key, value in validated_data.items():
            if key != "user":
                setattr(instance, key, value)

        instance.save()
        return instance
