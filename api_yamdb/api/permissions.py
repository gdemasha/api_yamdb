from rest_framework.permissions import SAFE_METHODS, BasePermission


class AuthorOrModeratorOrAdminPermission(BasePermission):
    """
    Кастомный пермишен для отзывов и комментариев.
    При безопасном методе доступ разрешен всем пользователям,
    при 'POST' - всем аутентифицированным,
    при 'DELETE', 'PATCH' - автору, админу и модератору.
    """

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user
            or request.method in SAFE_METHODS
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )


class AdminUserPermission(BasePermission):
    """
    Кастомный пермишен, разрешающий доступ любому пользователю
    при безопасном методе запроса, в иных случаях - только администратору.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return request.user.is_staff or request.user.role == 'admin'
        return False


class AdminOnlyPermission(BasePermission):
    """Кастомный пермишен, разрешающий доступ только администратору."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.is_staff or request.user.role == 'admin'
        return False
