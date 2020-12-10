from rest_framework.permissions import BasePermission

class CartPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_normal)

    def has_object_permission(self, request, view, obj):

        return request.user.is_authenticated and (request.user.is_normal or request.user.is_staff)

class IsCartHolder(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.user == request.user