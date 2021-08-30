from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User, Profile,Income,Expense


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["phone", "password"]
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attr):
        phone = attr.get('phone')
        password = attr.get('password')

        if phone and password:
            if User.objects.filter(phone=phone).exists():
                user = authenticate(request=self.context.get(
                    'request'), phone=phone, password=password)

            else:
                raise serializers.ValidationError(
                    'Phone number is not registered')

            if not user:
                msg = 'Unable to log in with provided credentials'
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = 'Must include "phone" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attr['user'] = user
        return attr


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class  IncomeSerializer(serializers.ModelSerializer):
    income=serializers.CharField
    amount=serializers.CharField
    class  Meta:
        model=Income
        fields='__all__'

class  ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Expense
        fields='__all__'