from rest_framework import permissions
from gazprominfo.gz import settings


class GetParameterPermission(permissions.BasePermission):
    """ Allows access to the view only if get parameter token equals to settings."""
    message = "Empty or wrong get parameter 'token'"

    def has_permission(self, request, view):
        return request.GET.get('token', "") == settings.GETPARAMETER_TOKEN
