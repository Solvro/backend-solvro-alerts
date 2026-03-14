from rest_framework import viewsets
from django.db.models import Q
from .models import Alert
from .serializers import AlertSerializer
from backend_solvro_alerts.permissions import IsAPIKeyAuthenticated
from django.utils import timezone


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
        Only returns alerts that are active and within the valid time range.
        """
        now = timezone.now()

        queryset = Alert.objects.filter(is_active=True)

        queryset = queryset.filter(Q(start_at__lte=now) | Q(start_at__isnull=True))

        queryset = queryset.filter(Q(end_at__gte=now) | Q(end_at__isnull=True))

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
