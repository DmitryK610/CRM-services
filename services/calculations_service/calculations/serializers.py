from rest_framework import serializers
from .models import Calculation, CalculationItem

class CalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculation
        fields = '__all__'

class CalculationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculationItem
        fields = '__all__'
