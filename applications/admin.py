from django.contrib import admin, messages
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    # Wyświetlamy tylko nazwę i daty, api_key jako hash jest mało użyteczny na liście
    list_display = ("name", "id", "created_at")

    # Ważne: api_key ustawiamy jako readonly, żeby admin nie mógł go wpisać ręcznie
    readonly_fields = ("id", "api_key", "created_at", "updated_at")

    def save_model(self, request, obj, form, change):
        """
        Nadpisujemy zapis, aby wygenerować klucz tylko przy tworzeniu nowej aplikacji.
        """
        if not change:  # Jeśli to nowy obiekt (nie edycja istniejącego)
            # Wywołujemy Twoją metodę z modelu, która hashue klucz i zwraca plain text
            plain_text_key = obj.generate_api_key()

            # Wyświetlamy duży, wyraźny komunikat na górze strony po zapisie
            messages.add_message(
                request,
                messages.WARNING,  # Używamy WARNING, żeby kolor rzucał się w oczy
                f"APLIKACJA UTWORZONA. Skopiuj klucz API teraz, nie zostanie on pokazany ponownie: {plain_text_key}",
            )

        # Standardowy zapis obiektu do bazy
        super().save_model(request, obj, form, change)

    # Definiujemy, co admin widzi w formularzu dodawania
    def get_fields(self, request, obj=None):
        if obj:  # Tryb edycji
            return ["name", "id", "api_key", "created_at", "updated_at"]
        return ["name"]  # Tryb tworzenia - admin widzi tylko pole 'name'
