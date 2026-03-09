from rest_framework import permissions
from .services.hashing import hash_string
from applications.models import Application


class IsAPIKeyAuthenticated(permissions.BasePermission):
    """
    Authentication class used for verifying app based on API key
    """

    message = "Invalid or missing API key"

    def has_permission(self, request, view):
        plain_text_api_key = request.META.get("HTTP_X_API_KEY")

        if not plain_text_api_key:
            return False

        hashed_api_key = hash_string(plain_text_api_key)

        # find an application by its hashed api key
        app = Application.objects.filter(api_key=hashed_api_key).first()

        if not app:
            return False

        # use safe verification
        return app.verify_api_key(plain_text_api_key)
