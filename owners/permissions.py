from rest_framework import permissions
from rest_framework.views import Request, View
from owners.models import Owner


class IsSuperUserOrUserOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Owner):
        return request.user.is_superuser or obj.user == request.user
