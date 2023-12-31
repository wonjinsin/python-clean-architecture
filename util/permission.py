from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request: object, view: object, obj: object) -> bool:
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user


class ReadOnly(BasePermission):
    def has_permission(self, request: object, view: object) -> bool:
        return request.method in SAFE_METHODS
