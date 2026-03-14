from django.contrib import admin
from .models import Alert


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    # Columns displayed in the list view of the admin panel
    list_display = ("title", "alert_type", "is_active", "is_global", "start_at")

    list_filter = ("is_active", "is_global", "alert_type")

    search_fields = ("title", "content")

    # UI widget for managing ManyToMany relationships
    filter_horizontal = ("applications",)
