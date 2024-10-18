from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "reset_password",
            "is_superuser",
            "is_active",
            "date_joined",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data: dict):
        if validated_data["is_superuser"]:
            return User.objects.create_superuser(**validated_data)
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict):
        reset_password = validated_data.get("reset_password")
        can_update_password = reset_password or instance.is_superuser

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
