
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AuditLog

class AuditLogCreateView(APIView):
	"""API для записи действия в аудит"""
	def post(self, request):
		data = request.data
		audit_log = AuditLog.objects.create(
			user=data.get('user'),
			action=data.get('action'),
			object_type=data.get('object_type'),
			object_id=data.get('object_id'),
			details=data.get('details')
		)
		return Response({"id": audit_log.id, "status": "created"}, status=status.HTTP_201_CREATED)
