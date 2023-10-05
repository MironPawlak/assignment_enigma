from rest_framework import permissions
from .models import CustomUser


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == CustomUser.CUSTOMER) or request.user.is_superuser


class IsSellerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.role == CustomUser.SELLER) or request.user.is_superuser


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.user.role == CustomUser.SELLER) or request.user.is_superuser
