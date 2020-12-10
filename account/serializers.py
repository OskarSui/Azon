from django.contrib.auth import authenticate
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from account.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=1, required=True, write_only=True)
    password_confirm = serializers.CharField(min_length=1, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm', 'name', 'is_normal')

    @staticmethod
    def validate_email(value):
        """здесь мы проверяем пароли на схожесть"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email already exist')
        return value

    def validate(self, data):
        """здесь мы проверяем поля которые зависят друг от друга а точнее пароль и его потдверждение. метод принимает словарь data в котором нам приходят все данные пользователя"""
        password = data.get('password')
        password_confirmation = data.pop('password_confirm')
        if password != password_confirmation:
            raise serializers.ValidationError("Passwords does not same")
        return data

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

# class LoginSerializer(TokenObtainPairSerializer):
#     """Этот класс нужен для логина после подтверждения аккаунта"""
#     email = serializers.EmailField()
#     password = serializers.CharField(trim_whitespace=False, write_only=True)


class RefreshTokenSerializer(TokenRefreshSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False, write_only=True)


    def validate(self, data):
        """Проверяем здесь на наличие пароля и почты"""
        email = data.get('email')
        print(email)
        password = data.get('password')
        print(password)
        print(self.context['request'])

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            print(user)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data