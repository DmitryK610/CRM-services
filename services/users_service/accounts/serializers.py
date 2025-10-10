from rest_framework import serializers
from .models import User, Role, Permission


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
            'email',
            'phone',
            'role',
            'permissions',
            'is_active',
            'is_staff',
            'is_superuser',
            'registered_at',
            'last_login',
            'password',
        ]
        read_only_fields = ['is_superuser', 'registered_at', 'last_login']

    def create(self, validated_data):
        permissions = validated_data.pop('permissions', [])
        password = validated_data.pop('password', None)
        user = User(**validated_data)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save()
        if permissions:
            user.permissions.set(permissions)
        return user

    def update(self, instance, validated_data):
        permissions = validated_data.pop('permissions', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()

        if permissions is not None:
            instance.permissions.set(permissions)

        return instance

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'