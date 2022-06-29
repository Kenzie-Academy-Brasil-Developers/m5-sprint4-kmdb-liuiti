from rest_framework import permissions

class ReviewListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

class ReviewDeletePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, review):
        return request.user.is_superuser or review.critic == request.user