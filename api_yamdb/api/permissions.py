from rest_framework.permissions import BasePermission, SAFE_METHODS


class AuthorOrModeratorOrAdminPermission(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in SAFE_METHODS
            or request.user.is_staff == request.user.is_authenticated
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )


class AdminUserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return request.user.is_staff or request.user.role == 'admin'
        return False


class AdminOnlyPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == 'admin'
        return False

