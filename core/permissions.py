from rest_framework import permissions, exceptions
from authentication.models import User

class HackathonPermissions(permissions.BasePermission):
        """
        1. GET can be accessed even by anonymous users
        2. PUT, PATCH and DELETE can only be accessed by the Super User
        """
        def has_permission(self, request, view):
            if request.method in permissions.SAFE_METHODS:
                return True
            return bool(request.user and request.user.is_superuser)

class AllowCompleteProfile(permissions.BasePermission):
    """
    1. GET can be accessed even by anonymous users
    2. POST can only be accessed by users whose profile is completed
    """
    def has_permission(self, request, view):
        user = request.user
        if((user.username != '') and (user.email !='') and (user.name != '') and (user.college != '')
            and (user.github_handle != '') and (user.bio != '') and (user.interests != '')):
            return True
        else:
            raise exceptions.PermissionDenied("Please complete your profile!")
