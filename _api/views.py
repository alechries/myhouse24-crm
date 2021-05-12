from _db import models
from . import serializers
from rest_framework import generics
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


class SectionList(generics.ListAPIView):
    model = models.House
    queryset = models.Section.objects.all()
    serializer_class = serializers.SectionSerializer


class SectionDetail(generics.RetrieveAPIView):
    model = models.Section
    queryset = models.Section.objects.all()
    serializer_class = serializers.SectionSerializer
