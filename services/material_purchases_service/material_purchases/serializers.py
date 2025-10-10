from rest_framework import serializers

from .models import MaterialPurchase


class MaterialPurchaseSerializer(serializers.ModelSerializer):
	class Meta:
		model = MaterialPurchase
		fields = '__all__'
