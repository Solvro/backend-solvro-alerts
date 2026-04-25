from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_revoked", "created_at")
    list_editable = ("is_revoked",)
    list_display_links = ("id",)

    # Read-only fields
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
        "api_key_actions",
    )

    # Form fields definition
    def get_fields(self, request, obj=None):
        if obj:  # Edit mode
            return [
                "name",
                "is_revoked",
                "api_key_actions",
                "id",
                "created_at",
                "updated_at",
            ]
        return ["name"]  # Create mode

    # 1. Regenerate button inside the edit form
    @admin.display(description="API Key")
    def api_key_actions(self, obj):
        if not obj.pk:
            return "Save the application to manage the API key."

        return mark_safe(
            '<button type="submit" name="_regenerate_key" class="button" '
            'style="background-color: #ba2121; color: white; padding: 6px 12px; '
            'font-weight: bold; cursor: pointer; border-radius: 4px; border: none;">'
            "⚠️ Regenerate API Key (Saves changes)</button>"
        )

    # 2. Helper for the copy-to-clipboard message
    def get_copy_message(self, key, action_text):
        return mark_safe(f"""
            <span style="display: inline-flex; align-items: center; gap: 12px; vertical-align: middle;">
                <strong>{action_text}</strong>
                <button type="button" 
                    onclick="navigator.clipboard.writeText('{key}').then(() => {{ 
                        this.innerText='✅ Copied!'; 
                        this.style.backgroundColor='#28a745'; 
                        this.style.color='white'; 
                        this.style.borderColor='#28a745';
                    }});"
                    style="margin: 0; padding: 4px 12px; cursor: pointer; border-radius: 4px; 
                    border: 1px solid #ccc; font-weight: bold; background-color: #fff; 
                    color: #333; font-size: 13px; display: inline-flex; align-items: center;">
                    📋 Copy API Key
                </button>
            </span>
        """)

    # 3. Save logic
    def save_model(self, request, obj, form, change):
        # Scenario: Creating a new application
        if not change:
            plain_text_key = obj.generate_api_key()
            messages.add_message(
                request,
                messages.WARNING,
                self.get_copy_message(plain_text_key, "Application created."),
            )

        # Scenario: Regenerate button clicked
        elif "_regenerate_key" in request.POST:
            plain_text_key = obj.generate_api_key()
            messages.add_message(
                request,
                messages.WARNING,
                self.get_copy_message(
                    plain_text_key, f"New key generated for '{obj.name}'."
                ),
            )

        super().save_model(request, obj, form, change)
