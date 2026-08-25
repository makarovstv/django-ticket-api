from rest_framework import permissions


class IsOwnerOrManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_manager:
            return True
        return obj.author == request.user


class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_manager


class IsAssigneeOrManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_manager:
            return True
        return obj.assignee == request.user
