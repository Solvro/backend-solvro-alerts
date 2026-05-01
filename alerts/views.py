from django.db.models import Q
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from applications.models import Application

from .models import Alert
from .serializers import AlertSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="app",
            type=str,
            location=OpenApiParameter.QUERY,
            required=False,
            description=(
                "Application code (e.g. 'testownik', 'topwr'). When provided, "
                "returns global alerts plus alerts targeted at that "
                "application. When omitted, only global alerts are returned."
            ),
        )
    ]
)
class AlertViewSet(viewsets.ReadOnlyModelViewSet):
    """Public, read-only endpoint exposing currently active alerts."""

    serializer_class = AlertSerializer
    permission_classes = []
    authentication_classes = []

    def get_queryset(self):
        now = timezone.now()
        qs = (
            Alert.objects.filter(is_active=True)
            .filter(Q(start_at__lte=now) | Q(start_at__isnull=True))
            .filter(Q(end_at__gt=now) | Q(end_at__isnull=True))
        )

        app_code = self.request.query_params.get("app")
        if app_code:
            if not Application.objects.filter(code=app_code).exists():
                raise ValidationError(
                    {"app": [f"Unknown application code: {app_code!r}."]}
                )
            return qs.filter(
                Q(is_global=True) | Q(applications__code=app_code)
            ).distinct()
        return qs.filter(is_global=True)
