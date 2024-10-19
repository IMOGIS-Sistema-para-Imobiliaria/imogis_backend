from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User


class IsSuperUserOrOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User):
        return (
            request.user.is_superuser or request.user.username == obj.username
        )
