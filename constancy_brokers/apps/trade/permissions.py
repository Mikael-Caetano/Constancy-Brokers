from rest_framework import permissions


class IsProviderAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_provider_admin