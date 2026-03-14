from rest_framework import viewsets
from django.db.models import Q
from .models import Alert
from .serializers import AlertSerializer
from backend_solvro_alerts.permissions import IsAPIKeyAuthenticated


class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing active alerts.

    Returns a list of alerts filtered by application name or global status.
    Requires a valid X-API-KEY header for authentication.
    """

    serializer_class = AlertSerializer
    permission_classes = [IsAPIKeyAuthenticated]

    def get_queryset(self):
        """
        Filter the available alerts based on the 'app' query parameter.
        Only returns active alerts.
        """
        queryset = Alert.objects.filter(is_active=True)

        # Retrieve the application name from query parameters (e.g., ?app=testownik)
        app_name = self.request.query_params.get("app")

        if app_name:
            # Filter: show alerts that are either global OR specifically assigned to this app
            queryset = queryset.filter(
                Q(is_global=True) | Q(applications__name=app_name)
            ).distinct()
        else:
            queryset = queryset.filter(is_global=True)

        return queryset
