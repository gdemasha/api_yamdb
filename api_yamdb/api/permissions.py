from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorOrModeratorOrAdminPermission(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return obj.author == request.user
        elif request.method == 'PATCH' or request.method == 'DELETE':
            return (
                obj.author == request.user
                or request.user.is_staff == request.user
                or request.user.role == 'moderator'
                or request.user.role == 'admin'
            )
        return True


class AdminUserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_staff == request.user
            or request.user.role == 'admin'
        )
