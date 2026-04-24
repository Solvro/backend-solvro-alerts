from rest_framework import viewsets
from backend_solvro_alerts.permissions import IsAPIKeyAuthenticated
import requests
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.conf import settings


class BaseAuthAPIViewSet(viewsets.ModelViewSet):
    """
    Base authentication class, viewsets based on this class require authentication using API key.
    """

    permission_classes = [IsAPIKeyAuthenticated]


def solvro_login(request):
    """Przekierowanie do Keycloak"""
    keycloak_url = f"{settings.SOLVRO_AUTH['KEYCLOAK_URL']}/realms/{settings.SOLVRO_AUTH['REALM']}/protocol/openid-connect/auth"

    params = {
        "client_id": settings.SOLVRO_AUTH["CLIENT_ID"],
        "redirect_uri": request.build_absolute_uri("/auth/callback/"),
        "response_type": "code",
        "scope": "openid email profile",
    }

    query_string = "&".join([f"{k}={v}" for k, v in params.items()])
    return redirect(f"{keycloak_url}?{query_string}")


def solvro_callback(request):
    """Obsługa callback z Keycloak"""
    code = request.GET.get("code")

    if not code:
        return redirect("/login/?error=no_code")

    # Wymiana kodu na token
    token_url = f"{settings.SOLVRO_AUTH['KEYCLOAK_URL']}/realms/{settings.SOLVRO_AUTH['REALM']}/protocol/openid-connect/token"

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": request.build_absolute_uri("/auth/callback/"),
        "client_id": settings.SOLVRO_AUTH["CLIENT_ID"],
        "client_secret": settings.SOLVRO_AUTH["CLIENT_SECRET"],
    }

    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()

    access_token = token_json.get("access_token")

    if not access_token:
        return redirect("/login/?error=no_token")

    # Pobranie informacji o użytkowniku
    userinfo_url = f"{settings.SOLVRO_AUTH['KEYCLOAK_URL']}/realms/{settings.SOLVRO_AUTH['REALM']}/protocol/openid-connect/userinfo"

    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_response = requests.get(userinfo_url, headers=headers)
    userinfo = userinfo_response.json()

    # Stworzenie lub pobranie użytkownika
    user, created = User.objects.get_or_create(
        username=userinfo["preferred_username"],
        defaults={
            "email": userinfo["email"],
            "first_name": userinfo.get("given_name", ""),
            "last_name": userinfo.get("family_name", ""),
        },
    )

    login(
        request, user, backend="django.contrib.auth.backends.ModelBackend"
    )  # somehow this works

    return redirect("/admin")
