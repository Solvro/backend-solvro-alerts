import uuid

from django.db import models


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
    title = models.CharField(max_length=255)
    alert_type = models.TextField(
        max_length=20, choices=AlertType.choices, default=AlertType.INFO
    )

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    is_global = models.BooleanField()
    is_active = models.BooleanField()
