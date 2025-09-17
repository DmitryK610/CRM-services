
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Material, Supplier
from .serializers import MaterialSerializer, SupplierSerializer
from .pagination import StandardPagination

def get_current_user(request):
	return getattr(request, 'user', None)

class MaterialViewSet(viewsets.ModelViewSet):
	queryset = Material.objects.all()
	serializer_class = MaterialSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['material_name', 'color_code', 'note']
	ordering_fields = ['material_name', 'cost', 'created_at']
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


class SupplierViewSet(viewsets.ModelViewSet):
	queryset = Supplier.objects.all()
	serializer_class = SupplierSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['company_name', 'contact_person', 'email', 'supplier_address', 'phone', 'note']
	ordering_fields = ['company_name', 'created_at']
	pagination_class = StandardPagination
