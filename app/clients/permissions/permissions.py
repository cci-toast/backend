from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS


class IsAuthenticatedOrWriteOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in ['POST'] or
            request.user and
            request.user.is_authenticated
        )


class ChangeItSelfOnly(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.method in ('POST',) or
            (request.user and
             request.user.is_authenticated and
             obj.user == request.user)
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_staff
