from rest_framework import permissions

class HackathonPermissions(permissions.BasePermission):
        '''
        1. GET can be accessed even by anonymous users
        2. PUT, PATCH and DELETE can only be accessed by the Super User
        '''
        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                return True
            return bool(request.user and request.user.is_superuser)
    