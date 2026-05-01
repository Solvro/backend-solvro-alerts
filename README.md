# Solvro Alerts

Centralny mikroserwis komunikatów / banerów dla aplikacji Solvro.
Frontendy (Testownik, Planer, Eventownik, …) odpytują jeden publiczny
endpoint i wyświetlają aktywne alerty użytkownikom.

Hostowane: <https://alerts.solvro.pl> — przewodnik integracji,
dokumentacja API (`/scalar/`) i panel admina (`/admin/`).

### Stack

- Django 6 · Django REST Framework · drf-spectacular (+ Scalar UI)
- django-unfold (themed admin) · custom email-based User model
- nh3 dla sanitizacji HTML alertów
- Solvro Auth (Keycloak / OIDC) jako alternatywne logowanie
- PostgreSQL na produkcji (`psycopg[binary]`), SQLite domyślnie w dev

### Instalacja

1. **Sklonuj repozytorium**

   ```bash
   git clone https://github.com/Solvro/backend-solvro-alerts
   cd backend-testownik
   ```

2. **Utwórz i aktywuj środowisko wirtualne**

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Linux / macOS
   .venv\Scripts\activate           # Windows
   ```

3. **Zainstaluj zależności**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Skopiuj plik środowiskowy**

   ```
   cp .env.example .env
   ```

5. **Wykonaj migracje bazy danych**

   ```bash
   python manage.py migrate
   ```

6. **(Opcjonalnie) Stwórz konto administratora**

   ```bash
   python manage.py createsuperuser
   ```

7. **Uruchom serwer deweloperski**

   ```bash
   python manage.py runserver
   ```
### Contributors

- [Wiktor Gruszczyński](https://github.com/WiktorGruszczynski)
- [Harukume](https://github.com/Harukume)
- [Antoni Czaplicki](https://github.com/Antoni-Czaplicki)
