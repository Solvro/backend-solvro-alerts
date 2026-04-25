import uuid

from django.db import models
from applications.models import Application


class AlertType(models.TextChoices):
    INFO = "info", "Info"
    WARNING = "warning", "Warning"
    CRITICAL = "critical", "Critical"


class Alert(models.Model):
    """
    Alert model.

    This model is used for alerting specified applications
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(default="")

    alert_type = models.CharField(
        max_length=20, choices=AlertType.choices, default=AlertType.INFO
    )

    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)

    is_global = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    applications = models.ManyToManyField(
        Application, related_name="alerts", blank=True
    )
