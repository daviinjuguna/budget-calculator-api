from django.shortcuts import render

from rest_framework import permissions, generics, status
from knox.models import AuthToken
from rest_framework.response import Response

from .models import User, Profile
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, ProfileSerializer
# Create your views here.


class LoginApi(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        profile = Profile.objects.filter(user=user).first()

        if user:
            return Response({
                'user': UserSerializer(user, many=False).data,
                'profile': ProfileSerializer(profile, many=False).data,
                "token": AuthToken.objects.create(user)[1]
            })
        else:
            return Response({
                "message": "UnAuthorised Access"
            }, status=status.HTTP_403_FORBIDDEN)


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):

        phone = request.data.get('phone', False)
        password = request.data.get('password', False)
        name = request.data.get('name', False)

        if phone and password:
            phone = str(phone)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({
                    "message": "User already exist"
                }, status=status.HTTP_403_FORBIDDEN)
            else:
                Temp_data = {'phone': phone, 'password': password}
                serializer = self.get_serializer(data=Temp_data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                user.save()

                profile = Profile(user=user, name=name)
                profile.save()

                print(user)
                return Response({
                    'user': UserSerializer(user, many=False).data,
                    'profile': ProfileSerializer(profile, many=False).data,
                    "token": AuthToken.objects.create(user)[1]
                })
        else:
            return Response({
                "message": "Either phone or password was not recieved "
            }, status=status.HTTP_403_FORBIDDEN)

        # try:
        #     phone = request.data.get('phone', False)
        #     password = request.data.get('password', False)

        #     if phone and password:
        #         phone = str(phone)
        #         user = User.objects.filter(phone__iexact=phone)
        #         if user.exists():
        #             return Response({
        #                 "message": "User already exist"
        #             }, status=status.HTTP_403_FORBIDDEN)
        #         else:
        #             #!Hsidetect password, inatuma error password required
        #             Temp_data = {'phone': phone, 'password': password}
        #             serializer = self.get_serializer(data=Temp_data)
        #             serializer.is_valid(raise_exception=True)
        #             user = serializer.save()
        #             user.save()

        #             return Response({
        #                 'user': UserSerializer(user, many=False).data,
        #                 "token": AuthToken.objects.create(user)[1]
        #             })
        #     else:
        #         return Response({
        #             "message": "Either phone or password was not recieved "
        #         }, status=status.HTTP_403_FORBIDDEN)
        # except Exception as e:
        #     print(e)
        #     return Response({
        #         "message": "Could not register user"
        #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
