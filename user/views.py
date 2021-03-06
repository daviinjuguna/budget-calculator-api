from django.shortcuts import render

from rest_framework import permissions, generics, status
from knox.models import AuthToken
from rest_framework.response import Response
from django.core.paginator import Paginator
from .common import initExpense

import json

from .models import User, Profile, Income, Expense
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, ProfileSerializer, IncomeSerializer, ExpenseSerializer
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
                initExpense(user)
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


class IncomeApi(generics.RetrieveAPIView):
    '''Income Api GET POST PUT DELETE'''

    serializer_class = IncomeSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        user = self.request.user
        offset = 25
        queryset = Income.objects.filter(user=user)
        paginator = Paginator(queryset, offset)
        page = self.request.query_params.get("page")
        pageList = paginator.get_page(page)
        last_page = paginator.num_pages
        total = 0.0
        for income in queryset:
            total = total + income.amount

        return Response({
            'income': IncomeSerializer(pageList, many=True).data,
            'total': total,
            "last_page": last_page,

        })

    def post(self, request):
        user = self.request.user
        json_data = json.loads(request.body)
        income = Income(
            user=user, income=json_data['income'], amount=float(json_data['amount']))
        income.save()

        return Response({
            "income": IncomeSerializer(income, many=False).data,
            "message": "Saved"
        })

    def put(self, request):
        json_data = json.loads(request.body)
        income = Income.objects.get(id=json_data['id'])
        income.income = json_data['income']
        income.amount = float(json_data['amount'])
        income.save()

        return Response({
            "income": IncomeSerializer(income, many=False).data,
            "message": "Edited"
        })

    def delete(self, request):
        id = self.request.query_params.get("income_id")
        income = Income.objects.get(id=id)
        income.delete()

        return Response({
            "message": "Income has been deleted",
        }, status=status.HTTP_204_NO_CONTENT)


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ExpenseApi(generics.RetrieveAPIView):
    '''Expneses api'''
    serializer_class = ExpenseSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request):
        user = self.request.user
        offset = 25
        queryset = Expense.objects.filter(user=user)
        paginator = Paginator(queryset, offset)
        page = self.request.query_params.get("page")
        pageList = paginator.get_page(page)
        last_page = paginator.num_pages
        total = 0.0
        for income in queryset:
            total = total + income.amount

        return Response({
            'expense': ExpenseSerializer(pageList, many=True).data,
            'total': total,
            "last_page": last_page,
        })

    def post(self, request):
        user = self.request.user
        json_data = json.loads(request.body)
        expense = Expense(recommended=json_data['recommended'],
                          user=user, expense=json_data['expense'], amount=float(json_data['amount']), static=json_data['static'],)
        expense.save()

        return Response({
            'expense': ExpenseSerializer(expense, many=False).data,
            "message": "Saved",
        })

    def put(self, request):
        json_data = json.loads(request.body)
        expense = Expense.objects.get(id=json_data['id'])
        expense.expense = json_data['expense']
        expense.amount = json_data['amount']
        expense.recommended = json_data['recommended']
        expense.amount = float(json_data['amount'])
        expense.static = json_data['static']
        expense.save()

        return Response({
            'expense': ExpenseSerializer(expense, many=False).data,
            "message": "Edited",
        })

    def delete(self, request):
        id = self.request.query_params.get("expense_id")
        expense = Expense.objects.get(id=id)
        expense.delete()

        return Response({
            "message": "Income has been deleted",
        }, status=status.HTTP_204_NO_CONTENT)
