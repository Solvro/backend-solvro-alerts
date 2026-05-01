import uuid

import nh3
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CheckConstraint, Q

from applications.models import Application

ALERT_HTML_TAGS = {
    "a",
    "b",
    "blockquote",
    "br",
    "code",
    "del",
    "div",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "li",
    "ol",
    "p",
    "pre",
    "s",
    "span",
    "strong",
    "sub",
    "sup",
    "u",
    "ul",
}
ALERT_HTML_ATTRS = {"a": {"href", "title", "target"}}
ALERT_URL_SCHEMES = {"http", "https", "mailto"}


def sanitize_alert_html(value: str) -> str:
    if not value:
        return ""
    return nh3.clean(
        value,
        tags=ALERT_HTML_TAGS,
        attributes=ALERT_HTML_ATTRS,
        url_schemes=ALERT_URL_SCHEMES,
    )


class AlertType(models.TextChoices):
    INFO = "info", "Info"
    WARNING = "warning", "Warning"
    CRITICAL = "critical", "Critical"


class Alert(models.Model):
    """A message broadcast to one or more Solvro applications."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)

    alert_type = models.CharField(
        max_length=20, choices=AlertType.choices, default=AlertType.INFO
    )
    link = models.URLField(
        max_length=500,
        blank=True,
        help_text=(
            "Optional URL. When set, frontends should make the entire alert "
            "banner clickable and navigate here on click."
        ),
    )
    open_in_new_tab = models.BooleanField(
        default=True,
        help_text=(
            "If true, frontends should open the link in a new tab "
            '(target="_blank" rel="noopener"). Ignored when link is empty.'
        ),
    )

    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)

    is_global = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_dismissable = models.BooleanField(default=True)

    applications = models.ManyToManyField(
        Application, related_name="alerts", blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            CheckConstraint(
                condition=Q(end_at__isnull=True)
                | Q(start_at__isnull=True)
                | Q(end_at__gt=models.F("start_at")),
                name="alert_end_after_start",
            ),
        ]

    def __str__(self):
        return self.title or f"Alert {self.id}"

    def clean(self):
        super().clean()
        if self.start_at and self.end_at and self.end_at <= self.start_at:
            raise ValidationError({"end_at": "end_at must be after start_at."})

    def save(self, *args, **kwargs):
        self.content = sanitize_alert_html(self.content)
        super().save(*args, **kwargs)
