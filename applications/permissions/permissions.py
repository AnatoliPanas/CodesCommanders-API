from rest_framework.permissions import BasePermission, SAFE_METHODS

from applications.users.choices.role_type import RoleType


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            # print(request.user, "--------", obj.owner)
            return request.user == obj.owner or request.user.role == RoleType.ADMIN.name
