
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Pricelist, PricelistItem
from .serializers import PricelistSerializer, PricelistItemSerializer

class PricelistViewSet(viewsets.ModelViewSet):
	queryset = Pricelist.objects.all()
	serializer_class = PricelistSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['name']
	ordering_fields = ['created_at', 'name']

	def get_user_role(self):
		user = getattr(self.request, 'user', None)
		# Предполагается, что user.role_id ссылается на модель Role, где name='admin'
		if hasattr(user, 'role_id'):
			from users_service.accounts.models import Role
			try:
				role = Role.objects.get(id=user.role_id)
				return role.name
			except Role.DoesNotExist:
				return None
		return None

	def create(self, request, *args, **kwargs):
		if self.get_user_role() != 'admin':
			from rest_framework.response import Response
			from rest_framework import status
			return Response({'detail': 'Only admin can create pricelist.'}, status=status.HTTP_403_FORBIDDEN)
		return super().create(request, *args, **kwargs)

	def update(self, request, *args, **kwargs):
		if self.get_user_role() != 'admin':
			from rest_framework.response import Response
			from rest_framework import status
			return Response({'detail': 'Only admin can edit pricelist.'}, status=status.HTTP_403_FORBIDDEN)
		return super().update(request, *args, **kwargs)

	def partial_update(self, request, *args, **kwargs):
		if self.get_user_role() != 'admin':
			from rest_framework.response import Response
			from rest_framework import status
			return Response({'detail': 'Only admin can edit pricelist.'}, status=status.HTTP_403_FORBIDDEN)
		return super().partial_update(request, *args, **kwargs)

class PricelistItemViewSet(viewsets.ModelViewSet):
	queryset = PricelistItem.objects.all()
	serializer_class = PricelistItemSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['item_name', 'unit']
	ordering_fields = ['price', 'item_name', 'unit']
