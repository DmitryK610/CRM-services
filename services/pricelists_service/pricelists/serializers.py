from rest_framework import serializers
from .models import Pricelist, PricelistItem

class PricelistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricelist
        fields = '__all__'

class PricelistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricelistItem
        fields = '__all__'
