from _db import models
from datetime import datetime
from django.db.models import Q
from itertools import chain
from . import serializers
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


class HouseList(generics.ListAPIView):
    model = models.House
    queryset = models.House.objects.all()
    serializer_class = serializers.HouseSerializer


class HouseDetail(generics.RetrieveAPIView):
    model = models.House
    queryset = models.House.objects.all()
    serializer_class = serializers.HouseSerializer


class AccountList(generics.ListAPIView):
    model = models.Account
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer


class AccountDetail(generics.RetrieveAPIView):
    model = models.Account
    queryset = models.Account.objects.all()
    serializer_class = serializers.AccountSerializer


class UserList(generics.ListAPIView):
    model = models.User
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetail(generics.RetrieveAPIView):
    model = models.User
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class MeasureList(generics.ListAPIView):
    model = models.Measure
    queryset = models.Measure.objects.all()
    serializer_class = serializers.MeasureSerializer


class MeasureDetail(generics.RetrieveAPIView):
    model = models.Measure
    queryset = models.Measure.objects.all()
    serializer_class = serializers.MeasureSerializer


class SectionList(generics.ListAPIView):
    model = models.House
    serializer_class = serializers.SectionSerializer

    def get_queryset(self):
        queryset = models.Section.objects.all()
        house = self.request.query_params.get('house')
        if house is not None:
            queryset = queryset.filter(house=house)
        return queryset


class SectionDetail(generics.RetrieveAPIView):
    model = models.Section
    queryset = models.Section.objects.all()
    serializer_class = serializers.SectionSerializer


class FloorList(generics.ListAPIView):
    model = models.Floor
    serializer_class = serializers.FloorSerializer

    def get_queryset(self):
        queryset = models.Floor.objects.all()
        section = self.request.query_params.get('section')
        if section is not None:
            queryset = queryset.filter(section=section)
        return queryset


class FloorDetail(generics.RetrieveAPIView):
    model = models.Floor
    queryset = models.Floor.objects.all()
    serializer_class = serializers.FloorSerializer


class ApartmentList(generics.ListAPIView):
    model = models.Apartment
    serializer_class = serializers.ApartmentSerializer

    def get_queryset(self):
        queryset = models.Apartment.objects.all()

        floor = self.request.query_params.get('floor')
        account = self.request.query_params.get('account')
        user = self.request.query_params.get('user')

        if floor is not None:
            queryset = queryset.filter(floor=floor)

        elif account is not None:
            queryset = queryset.filter(account=account)

        elif user is not None:
            queryset = queryset.filter(user=user)

        return queryset


class ApartmentDetail(generics.RetrieveAPIView):
    model = models.Apartment
    queryset = models.Apartment.objects.all()
    serializer_class = serializers.ApartmentSerializer


class ServiceList(generics.ListAPIView):
    model = models.Service
    serializer_class = serializers.ServiceSerializer

    def get_queryset(self):
        queryset = models.Service.objects.all()
        measure = self.request.query_params.get('measure')
        if measure is not None:
            queryset = queryset.filter(measure=measure)
        return queryset


class ServiceDetail(generics.RetrieveAPIView):
    model = models.Service
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer


class TariffServiceList(generics.ListAPIView):
    model = models.TariffService
    serializer_class = serializers.TariffServiceSerializer

    def get_queryset(self):
        queryset = models.TariffService.objects.all()

        tariff = self.request.query_params.get('tariff')
        service = self.request.query_params.get('service')
        if tariff is not None:
            queryset = queryset.filter(tariff=tariff)
        elif service is not None:
            queryset = queryset.filter(service=service)

        return queryset


class TariffServiceDetail(generics.RetrieveAPIView):
    model = models.TariffService
    queryset = models.TariffService.objects.all()
    serializer_class = serializers.TariffServiceSerializer


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, response):
        current_year = datetime.now().year
        months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        input_invoice_data = []
        output_invoice_data = []
        output_transfer_data = []
        input_transfer_data = []
        for month in months:
            invoice_in = models.Invoice.objects.filter(Q(date__month=months[month - 1], date__year=current_year),
                                                       Q(type='Оплачена'))
            invoice_out = models.Invoice.objects.filter(Q(date__month=months[month - 1], date__year=current_year),
                                                        Q(type='Неоплачена'))
            transfer_out = models.Transfer.objects.filter(Q(created_date__month=months[month - 1]),
                                                          Q(solo_status=0), created_date__year=current_year)
            transfer_in = models.Transfer.objects.filter(Q(created_date__month=months[month - 1],
                                                           created_date__year=current_year),
                                                         (Q(solo_status=1) | Q(solo_status=None)))

            if transfer_out:
                total = 0
                for el in transfer_out:
                    total += el.amount
                output_transfer_data.append(total)
            else:
                output_transfer_data.append(0)

            if transfer_in:
                total = 0
                for el in transfer_in:
                    total += el.amount
                input_transfer_data.append(total)
            else:
                input_transfer_data.append(0)

            if invoice_in:
                total = 0
                for el in invoice_in:
                    total += el.total_amount
                input_invoice_data.append(total)
            else:
                input_invoice_data.append(0)

            if invoice_out:
                total = 0
                for el in invoice_out:
                    total += el.total_amount
                output_invoice_data.append(total)
            else:
                output_invoice_data.append(0)
        print(output_invoice_data)

        labels = ["Сентябрь", "Октябрь", "Ноябрь", "Декабрь", "Январь",
                  "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август"]
        data = {
            "labels": labels,
            'output_transfer': output_transfer_data,
            'input_transfer': input_transfer_data,
            'output_invoice': output_invoice_data,
            'input_invoice': input_invoice_data,
        }
        return Response(data)
