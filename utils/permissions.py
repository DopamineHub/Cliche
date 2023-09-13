from rest_framework import (
    exceptions,
    permissions,
)


class IsReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthenticated(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            # raise 401 instead of 403
            raise exceptions.NotAuthenticated('not authenticated')

        return True


class IsAdmin(IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

    def has_permission(self, request, view):
        return (
                super().has_permission(request, view) and
                request.user.is_staff
        )


IsAuthenticatedOrReadOnly = IsReadOnly | IsAuthenticated
IsAuthenticatedRead = IsReadOnly & IsAuthenticated
IsAdminOrReadOnly = IsReadOnly | IsAdmin
