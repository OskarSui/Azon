
from rest_framework.permissions import BasePermission
from rest_framework import permissions
# from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ProductPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_normal)

    def has_object_permission(self, request, view, obj):

        return request.user.is_authenticated and (request.user.is_normal or request.user.is_staff)

class IsProductAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author_id == request.user

class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author_id == request.user

class IsAuthenticatedOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
