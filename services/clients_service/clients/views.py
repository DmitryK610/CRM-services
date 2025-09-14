
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Client
from .serializers import ClientSerializer
from .pagination import StandardPagination

def get_current_user(request):
	# Пример получения пользователя, доработать под вашу авторизацию
	return getattr(request, 'user', None)

class ClientViewSet(viewsets.ModelViewSet):
	queryset = Client.objects.all()
	serializer_class = ClientSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['full_name', 'contact_phone', 'email', 'address', 'note']
	ordering_fields = ['full_name', 'created_at', 'updated_at']
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
