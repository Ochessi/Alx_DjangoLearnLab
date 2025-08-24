from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Allow read-only to anyone, but write/update/delete only to the author.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return hasattr(obj, 'author') and obj.author == request.user
