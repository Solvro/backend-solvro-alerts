from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget

from .models import Alert


@admin.register(Alert)
class AlertAdmin(ModelAdmin):
    list_display = (
        "title",
        "alert_type",
        "applications_display",
        "is_active",
        "is_global",
        "start_at",
        "end_at",
    )
    list_filter = (
        "applications",
        "is_active",
        "is_global",
        "is_dismissable",
        "alert_type",
    )
    search_fields = ("title", "content")
    autocomplete_fields = ("applications",)
    readonly_fields = ("id", "created_at", "updated_at")

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("applications")

    @admin.display(description="Applications")
    def applications_display(self, obj):
        names = list(obj.applications.values_list("name", flat=True))
        if names:
            return ", ".join(names)
        return "Global" if obj.is_global else "-"

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "content",
                    "alert_type",
                    "link",
                    "open_in_new_tab",
                    "is_dismissable",
                )
            },
        ),
        ("Targeting", {"fields": ("is_global", "applications")}),
        (
            "Schedule",
            {"fields": ("is_active", "start_at", "end_at")},
        ),
        (
            "Metadata",
            {"fields": ("id", "created_at", "updated_at")},
        ),
    )
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget(attrs={"style": "min-height: 18rem;"}),
        },
    }
