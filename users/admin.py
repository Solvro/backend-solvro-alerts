from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as DjangoGroupAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.models import Group
from unfold.admin import ModelAdmin
from unfold.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)

from .models import User

admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(DjangoGroupAdmin, ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(DjangoUserAdmin, ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    change_password_form = AdminPasswordChangeForm

    ordering = ("email",)
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_superuser",
    )
    list_filter = ("is_active", "is_superuser", "groups")
    search_fields = ("email", "first_name", "last_name")
    filter_horizontal = ("groups", "user_permissions")
    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    actions = ("approve_users",)

    @admin.action(description="Approve selected users (set is_active=True)")
    def approve_users(self, request, queryset):
        updated = queryset.filter(is_active=False).update(is_active=True)
        messages.success(request, f"Approved {updated} user(s).")
