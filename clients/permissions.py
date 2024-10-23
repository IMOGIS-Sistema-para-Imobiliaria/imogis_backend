from rest_framework import permissions
from rest_framework.views import Request, View
from .models import Client


class IsSuperUserOrUserClient(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Client):
        return request.user.is_superuser or obj.user == request.user
