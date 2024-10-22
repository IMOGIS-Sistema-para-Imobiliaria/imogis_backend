from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    user_fullname = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "user_fullname",
            "is_superuser",
            "is_active",
            "password",
            "last_login",
            "date_joined",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ]
            },
            "email": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="User with this email already exists.",
                    )
                ]
            },
        }

    def get_user_fullname(self, obj):
        return (
            f"{obj.first_name} {obj.last_name}"
            if obj.first_name and obj.last_name
            else None
        )

    def create(self, validated_data: dict):
        password = validated_data.pop("password", None)

        if validated_data.get("is_superuser"):
            user = User.objects.create_superuser(**validated_data)
        else:
            user = User.objects.create_user(**validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def update(self, instance: User, validated_data: dict):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance
