from rest_framework import permissions
from account.models import CustomUser

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and isinstance(request.user, CustomUser) and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Allow read-only access to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow modifications only if the user is the author
        return obj.user == request.user

class isAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the role 'volunteer'
        return request.user and isinstance(request.user, CustomUser) and request.user.is_authenticated and request.user.role == 'volunteer'

class isNormalUser(permissions.BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the role 'normal'
        return request.user and isinstance(request.user, CustomUser) and request.user.is_authenticated and request.user.role == 'normal'
