from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import MaterialPurchase
from .pagination import StandardPagination
from .serializers import MaterialPurchaseSerializer


def get_current_user(request):
	return getattr(request, 'user', None)


class MaterialPurchaseViewSet(viewsets.ModelViewSet):
	queryset = MaterialPurchase.objects.all()
	serializer_class = MaterialPurchaseSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['status', 'payment_method', 'notes']
	ordering_fields = ['purchase_order_date', 'total_cost', 'created_at']
	pagination_class = StandardPagination

	def perform_create(self, serializer):
		user = get_current_user(self.request)
		instance = serializer.save()
		instance._current_user = user
		return instance

	def perform_update(self, serializer):
		user = get_current_user(self.request)
		instance = serializer.save()
		instance._current_user = user
		return instance
