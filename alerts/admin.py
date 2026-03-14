from django.contrib import admin
from .models import Alert


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    # To, co będzie widać na liście wszystkich alertów
    list_display = ("title", "alert_type", "is_active", "is_global", "start_at")

    list_filter = ("is_active", "is_global", "alert_type")

    search_fields = ("title", "content")

    # Pozwala przypisywać aplikacje przez interfejs
    filter_horizontal = ("applications",)