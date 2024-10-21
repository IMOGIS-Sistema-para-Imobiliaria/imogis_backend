from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Owner


class OwnerSerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField(read_only=True)

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
            "last_updated_by",
            "type_of_sale",
            "user_fullname",
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
            "last_updated_by": {"read_only": True},
        }

    def get_user_fullname(self, obj):
        return (
            f"{obj.user.first_name} {obj.user.last_name}" if obj.user else None
        )

    def update(self, instance: Owner, validated_data: dict):
        instance.last_updated_by = (
            f"{validated_data.get('user', instance.user).first_name} "
            f"{validated_data.get('user', instance.user).last_name}"
        )

        for key, value in validated_data.items():
            if key != "user":
                setattr(instance, key, value)

        instance.save()
        return instance
