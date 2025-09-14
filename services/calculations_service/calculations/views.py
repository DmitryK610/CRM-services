
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Calculation, CalculationItem
from .serializers import CalculationSerializer, CalculationItemSerializer

class CalculationViewSet(viewsets.ModelViewSet):
	queryset = Calculation.objects.all()
	serializer_class = CalculationSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['name']
	ordering_fields = ['created_at', 'name']

class CalculationItemViewSet(viewsets.ModelViewSet):
	queryset = CalculationItem.objects.all()
	serializer_class = CalculationItemSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['item_name', 'unit']
	ordering_fields = ['price', 'item_name', 'unit', 'quantity', 'total']
