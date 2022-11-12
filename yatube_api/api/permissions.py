from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Проверка методов на безопасность для неавтора."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
        )
