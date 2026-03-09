from django.contrib import admin, messages
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

    list_editable = ("name",)

    list_display_links = ("id",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    def save_model(self, request, obj, form, change):
        if not change:
            plain_text_key = obj.generate_api_key()

            # Wyświetlamy duży, wyraźny komunikat na górze strony po zapisie
            messages.add_message(
                request,
                messages.WARNING,
                f"APLIKACJA UTWORZONA. Skopiuj klucz API teraz, nie zostanie on pokazany ponownie: {plain_text_key}",
            )

        # Standardowy zapis obiektu do bazy
        super().save_model(request, obj, form, change)

    # Definiujemy, co admin widzi w formularzu dodawania
    def get_fields(self, request, obj=None):
        if obj:  # Tryb edycji
            return ["name", "id", "created_at", "updated_at"]
        return ["name"]  # Tryb tworzenia - admin widzi tylko pole 'name'
