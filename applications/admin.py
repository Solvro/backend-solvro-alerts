from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(ModelAdmin):
    list_display = ("name", "code", "created_at", "updated_at")
    search_fields = ("name", "code")
    readonly_fields = ("id", "created_at", "updated_at")
    prepopulated_fields = {"code": ("name",)}
    fieldsets = (
        (None, {"fields": ("name", "code")}),
        (
            "Metadata",
            {"fields": ("id", "created_at", "updated_at")},
        ),
    )
