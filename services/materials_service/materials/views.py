
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Material
from .serializers import MaterialSerializer
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
