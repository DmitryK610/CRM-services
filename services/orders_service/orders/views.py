
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, OrderItemSerializer, PaymentSerializer
from .pagination import OrderPagination

def get_current_user(request):
	return getattr(request, 'user', None)

class OrderViewSet(viewsets.ModelViewSet):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = [
		'order_number', 'status', 'note'
	]
	ordering_fields = [
		'order_date', 'created_at', 'total_amount', 'status'
	]
	pagination_class = OrderPagination

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

class OrderItemViewSet(viewsets.ModelViewSet):
	queryset = OrderItem.objects.all()
	serializer_class = OrderItemSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['product_name']
	ordering_fields = ['quantity', 'unit_price', 'total_price']
	pagination_class = OrderPagination

class PaymentViewSet(viewsets.ModelViewSet):
	queryset = Payment.objects.all()
	serializer_class = PaymentSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['status', 'payment_method', 'transaction_id']
	ordering_fields = ['amount', 'payment_date', 'created_at']
	pagination_class = OrderPagination
