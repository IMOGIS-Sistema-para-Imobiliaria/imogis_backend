from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
            "reset_password",
            "is_superuser",
            "is_active",
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
                        message="user with this email already exists.",
                    )
                ]
            },
        }

    def create(self, validated_data: dict):
        if validated_data["is_superuser"]:
            return User.objects.create_superuser(**validated_data)
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict):
        # User making the request...
        req_user = self.context["request"].user

        is_resettable = instance.reset_password
        is_admin = req_user.is_superuser

        can_update_password = is_admin or is_resettable

        for key, value in validated_data.items():
            if key == "password" and can_update_password:
                instance.set_password(value)
                instance.reset_password = False
            elif key == "password" and not can_update_password:
                continue
            else:
                setattr(instance, key, value)

        instance.save()
        return instance
