from rest_framework import permissions

class IsAnonimousPermission (permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        return True
class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False