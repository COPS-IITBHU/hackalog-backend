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

class IsLeaderOrSuperUser(permissions.BasePermission):
    """
    Allows only Superusers and Creator of team to delete the team.
    """
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        else:
            raise exceptions.NotAuthenticated("Singin is required!")

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user == obj.leader:
            return True
        else:
            raise exceptions.PermissionDenied("You are not team leader")
