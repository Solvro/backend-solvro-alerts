import secrets
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_http_methods, require_safe

from .forms import RegisterForm
from .models import User

OAUTH_TIMEOUT = 5
SOLVRO_STATE_SESSION_KEY = "solvro_oauth_state"
SOLVRO_NEXT_SESSION_KEY = "solvro_oauth_next"


def _safe_next(request, fallback="/admin/"):
    next_url = request.GET.get("next") or request.POST.get("next") or fallback
    if not next_url.startswith("/") or next_url.startswith("//"):
        return fallback
    return next_url


@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect("/admin/")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account created. It must be approved by an administrator "
                "before you can log in.",
            )
            return redirect(reverse_lazy("admin:login"))
    else:
        form = RegisterForm()
    return render(request, "admin/register.html", {"form": form})


@require_safe
def solvro_login(request):
    state = secrets.token_urlsafe(32)
    request.session[SOLVRO_STATE_SESSION_KEY] = state
    request.session[SOLVRO_NEXT_SESSION_KEY] = _safe_next(request)

    cfg = settings.SOLVRO_AUTH
    auth_url = (
        f"{cfg['KEYCLOAK_URL']}/realms/{cfg['REALM']}/protocol/openid-connect/auth"
    )
    params = {
        "client_id": cfg["CLIENT_ID"],
        "redirect_uri": request.build_absolute_uri(reverse("solvro_callback")),
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
    }
    return redirect(f"{auth_url}?{urlencode(params)}")


@require_safe
def solvro_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")
    expected_state = request.session.pop(SOLVRO_STATE_SESSION_KEY, None)
    next_url = request.session.pop(SOLVRO_NEXT_SESSION_KEY, "/admin/")
    login_url = reverse_lazy("admin:login")

    if not code or not state or state != expected_state:
        messages.error(request, "Invalid Solvro Auth response. Please try again.")
        return redirect(login_url)

    cfg = settings.SOLVRO_AUTH
    token_url = (
        f"{cfg['KEYCLOAK_URL']}/realms/{cfg['REALM']}/protocol/openid-connect/token"
    )
    try:
        token_response = requests.post(
            token_url,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": request.build_absolute_uri(reverse("solvro_callback")),
                "client_id": cfg["CLIENT_ID"],
                "client_secret": cfg["CLIENT_SECRET"],
            },
            timeout=OAUTH_TIMEOUT,
        )
        token_response.raise_for_status()
        access_token = token_response.json().get("access_token")
        if not access_token:
            raise ValueError("missing access_token")

        userinfo_url = (
            f"{cfg['KEYCLOAK_URL']}/realms/{cfg['REALM']}"
            "/protocol/openid-connect/userinfo"
        )
        userinfo_response = requests.get(
            userinfo_url,
            headers={"Authorization": f"Bearer {access_token}"},
            timeout=OAUTH_TIMEOUT,
        )
        userinfo_response.raise_for_status()
        userinfo = userinfo_response.json()
    except (requests.RequestException, ValueError):
        messages.error(request, "Could not contact Solvro Auth. Please try again.")
        return redirect(login_url)

    email = (userinfo.get("email") or "").lower()
    if not email:
        messages.error(request, "Solvro Auth did not return an email address.")
        return redirect(login_url)

    user = User.objects.filter(email__iexact=email).first()
    created = user is None
    if created:
        user = User.objects.create(
            email=email,
            first_name=userinfo.get("given_name", ""),
            last_name=userinfo.get("family_name", ""),
            is_active=False,
        )
        user.set_unusable_password()
        user.save(update_fields=["password"])

    if created or not user.is_active:
        messages.warning(
            request,
            "Your account is pending administrator approval. "
            "You'll be able to sign in once an admin activates it.",
        )
        return redirect(login_url)

    login(request, user, backend="django.contrib.auth.backends.ModelBackend")
    return redirect(next_url)
