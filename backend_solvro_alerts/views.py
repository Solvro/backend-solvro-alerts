from rest_framework import viewsets
from backend_solvro_alerts.permissions import IsAPIKeyAuthenticated


class BaseAuthAPIViewSet(viewsets.ModelViewSet):
    """
    Base authentication class, viewsets based on this class require authentication using API key.
    """

    permission_classes = [IsAPIKeyAuthenticated]
