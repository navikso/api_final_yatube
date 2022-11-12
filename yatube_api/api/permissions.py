from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Автору доступны все методы.
    Для неавтора осуществляется проверка методов на безопасность.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )
