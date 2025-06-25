import re

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework import serializers

from applications.users.choices.role_type import RoleType
from applications.users.models.user import User

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'is_staff',
        ]


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=RoleType.choices(),
        required=True
    )
    is_staff = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'password',
            're_password',
            'email',
            'role',
            'is_staff'
        ]

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')
        email = attrs.get('email')

        re_pattern = r'^[a-zA-Z]+$'

        if not email:
            raise serializers.ValidationError({'email': 'Это поле является обязательным.'})

        try:
            validate_email(email)
        except ValidationError:
            raise serializers.ValidationError({'email': 'Пожалуйста, введите правильный адрес электронной почты.'})

        if not re.match(re_pattern, first_name):
            raise serializers.ValidationError(
                {"first_name": "Имя должно содержать только символы алфавита."}
            )

        if not re.match(re_pattern, last_name):
            raise serializers.ValidationError(
                {"last_name": "Фамилия должна содержать только символы алфавита."}
            )

        password = attrs.get('password')
        re_password = attrs.pop('re_password', None)

        if not password:
            raise serializers.ValidationError(
                {"password": "Это поле является обязательным."}
            )

        if not re_password:
            raise serializers.ValidationError(
                {"re_password": "Это поле является обязательным."}
            )

        validate_password(password)

        if password != re_password:
            raise serializers.ValidationError(
                {"re_password": "Пароль не совпадает."}
            )

        return attrs

    def create(self, validated_data):
        role = validated_data.get('role')
        validated_data['is_staff'] = role == RoleType.ADMIN.name

        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)

        user.save()

        return user

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(
        required=True,
        error_messages={
            'required': _('Поле username обязательно для заполнения'),
            'invalid': _('Введите корректное username')
        }
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        error_messages={
            'required': _('Поле password обязательно для заполнения'),
            'min_length': _('Пароль должен содержать минимум 8 символов')
        }
    )