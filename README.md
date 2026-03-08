## 🤝 Kontrybucja

Chcesz pomóc w rozwoju Testownika? Let's go!

1. Sforkuj repozytorium (tylko jeśli jeszcze nie jesteś w teamie testownika)
2. Stwórz branch dla swojej funkcji (`git checkout -b feat/amazing-feature`)
3. Commituj zmiany (`git commit -m 'feat: add amazing feature'`)
4. Wypchnij branch (`git push origin feature/amazing-feature`)
5. Otwórz Pull Request

Aby było nam wszystkim łatwiej stosuj się do tych zasad przy tworzeniu branchy oraz commitów.

### 🪾 Nazewnictwo branchy

Każdy branch powinien zawierać **prefiks określający typ zmiany** oraz **numer GitHub Issue**.

**Format**

```
<prefix>/<issue>-short-description
```

**Dostępne prefiksy**

- `feat/` - nowe funkcje
- `fix/` - poprawki błędów
- `hotfix/` - krytyczne poprawki produkcyjne
- `design/` - zmiany UI/UX
- `refactor/` - poprawa kodu bez zmiany działania
- `test/` - testy
- `docs/` - dokumentacja

**Przykłady**

```
feat/123-add-usos-integration
fix/87-token-refresh-bug
refactor/210-cleanup-serializers
```


### 🧹 Pre-commit i jakość kodu

W projekcie używamy [pre-commit](https://pre-commit.com/) oraz [ruff](https://docs.astral.sh/ruff/) do automatycznego formatowania i lintowania kodu przy każdym `git commit`.

**Instalacja narzędzi deweloperskich**

   ```bash
      pip install -r requirements-dev.txt
   ```

**Instalacja hooków pre-commit**

   ```bash
      pre-commit install
   ```

**Ręczne uruchomienie wszystkich hooków**

   ```bash
      pre-commit run --all-files
   ```


Po instalacji hooków, przy każdym `git commit` automatycznie uruchomią się:

- `ruff` – linting i sortowanie importów

- `ruff-format` – formatowanie kodu


### ✍️ Format commitów

Stosujemy standard [**Conventional Commits**](https://www.conventionalcommits.org/en/v1.0.0/), aby się móc później łatwiej połapać.

**Format**

```
<type>(opcjonalny scope): opis w czasie teraźniejszym
```

**Typy commitów**

- `feat:` - nowa funkcjonalność
- `fix:` - naprawa błędu
- `docs:` - dokumentacja
- `refactor:` - poprawa struktury kodu
- `test:` - testy
- `chore:` - zmiany w konfiguracji, dependency itp.

**Przykłady**

```bash
   feat(auth): add USOS SSO login
   fix(quizzes): correct question ordering
   docs: update README with backend setup
```
---
