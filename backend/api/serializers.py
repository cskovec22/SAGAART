from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import serializers

from api.utils import send_code_by_email
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""
    # favorite_style 
    # favorite_category
    # favorite_artist
    # subscription
    confirm_password = serializers.CharField(
        write_only=True
        # style={"input_type": "password"}
    )

    class Meta:
        """Конфигурация сериализатора для пользователя."""
        model = CustomUser
        fields = (
            # "id",
            "phone",
            "email",
            # "first_name",
            # "last_name",
            # "surname",
            "password",
            "confirm_password"
            # "favorite_style",
            # "favorite_category",
            # "favorite_artist",
            # "subscription"
        )
        extra_kwargs = {
            "password": {"write_only": True},
            # "password_repeat": {"write_only": True}
        }

    def validate(self, data):
        """Проверить, совпадают ли пароли."""
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"message": "Пароли не совпадают."}
            )
        try:
            validate_password(data["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"message": list(e.messages)})
        return data

    def create(self, validated_data):
        """Создать пользователя без повторного пароля."""
        validated_data.pop("confirm_password")
        user = CustomUser(**validated_data)
        user.set_password(validated_data["password"])

        email = validated_data["email"]
        user.username = email
        user.save()

        message = "Учетная запись создана."
        send_code_by_email(email, message)
        return user


class LoginSerializer(serializers.Serializer):
    """Сериализатор для входа пользователя по электронной почте и паролю."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True
    )

    # def validate(self, data):
    #     """Аутентификация пользователя о электронной почте и паролю."""
    #     user = authenticate(email=data["email"], password=data["password"])
    #     if not user:
    #         raise serializers.ValidationError(
    #             "Неверный адрес электронной почты или пароль."
    #         )
    #     return user
