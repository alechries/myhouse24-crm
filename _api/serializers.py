from _db import models
from rest_framework import serializers


class HouseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.House
        fields = ('id', 'user', 'name', 'address', 'number', 'image1', 'image2', 'image3', 'image4', 'image5', )


class SectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Section
        fields = ('id', 'house', 'name', )
