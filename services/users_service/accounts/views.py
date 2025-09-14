
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import User, Role, Permission
from .serializers import UserSerializer, RoleSerializer, PermissionSerializer
from .pagination import UserPagination

def get_current_user(request):
    return getattr(request, 'user', None)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['full_name', 'email', 'phone']
    ordering_fields = ['registered_at', 'last_login', 'is_active']
    pagination_class = UserPagination

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    pagination_class = UserPagination

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['code', 'name']
    ordering_fields = ['code', 'name']
    pagination_class = UserPagination
