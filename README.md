### Instrukcja użycia API

1. **Przykladowy request**

```bash
curl -X GET "http://localhost:8000/api/v1/alerts?app=testownik" \
     -H "X-API-KEY: YOUR_APPLICATION_API_KEY" \
     -H "Content-Type: application/json"
```

2. **Przykladowy resposne**
```json
[
  {
    "title": "System Maintenance",
    "content": "Planned downtime at 10 PM.",
    "alert_type": "info",
    "is_global": true
  },
  {
    "title": "App Specific Alert",
    "content": "Only for testownik app.",
    "alert_type": "warning",
    "is_global": false
  }
]
```

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
