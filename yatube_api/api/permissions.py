from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrAnyReadOnly(BasePermission):
    """
    Object-level permission to only allow authors of an object to edit it.
    Assumes the model instance has an `author` attribute.
    """

    def has_object_permission(self, request, view, obj):
        is_user = obj.author == request.user
        is_safe = request.method in SAFE_METHODS
        return is_safe or is_user
