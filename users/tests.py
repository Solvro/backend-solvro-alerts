from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .models import User


class IndexPageTests(TestCase):
    def test_index_renders(self):
        r = self.client.get(reverse("index"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Solvro Alerts")


class RegisterTests(TestCase):
    def test_register_creates_inactive_user(self):
        r = self.client.post(
            reverse("admin_register"),
            {
                "email": "alice@example.com",
                "first_name": "Alice",
                "last_name": "A",
                "password1": "SuperSafePass!23",
                "password2": "SuperSafePass!23",
            },
        )
        self.assertEqual(r.status_code, 302)
        user = User.objects.get(email="alice@example.com")
        self.assertFalse(user.is_active)
        self.assertEqual(user.email, "alice@example.com")


class UserModelTests(TestCase):
    def test_email_is_unique_and_lowercased(self):
        u = User.objects.create_user(email="Foo@Example.com", password="x")
        self.assertEqual(u.email, "foo@example.com")
        with self.assertRaises(Exception):
            User.objects.create_user(email="foo@example.com", password="x")


class SolvroAuthTests(TestCase):
    def test_login_redirects_to_keycloak_with_state(self):
        with self.settings(
            SOLVRO_AUTH={
                "KEYCLOAK_URL": "https://auth.example",
                "REALM": "solvro",
                "CLIENT_ID": "cid",
                "CLIENT_SECRET": "secret",
            }
        ):
            r = self.client.get(reverse("solvro_login"))
        self.assertEqual(r.status_code, 302)
        self.assertIn("auth.example", r["Location"])
        self.assertIn("state=", r["Location"])

    def test_callback_rejects_state_mismatch(self):
        session = self.client.session
        session["solvro_oauth_state"] = "expected"
        session.save()
        r = self.client.get(reverse("solvro_callback"), {"code": "x", "state": "wrong"})
        self.assertEqual(r.status_code, 302)
        self.assertFalse(User.objects.exists())

    def test_callback_creates_inactive_user_when_unknown(self):
        session = self.client.session
        session["solvro_oauth_state"] = "s"
        session["solvro_oauth_next"] = "/admin/"
        session.save()

        with (
            patch("users.views.requests.post") as p_post,
            patch("users.views.requests.get") as p_get,
        ):
            p_post.return_value.json.return_value = {"access_token": "tok"}
            p_post.return_value.raise_for_status.return_value = None
            p_get.return_value.json.return_value = {
                "email": "bob@example.com",
                "given_name": "Bob",
                "family_name": "B",
            }
            p_get.return_value.raise_for_status.return_value = None

            r = self.client.get(reverse("solvro_callback"), {"code": "x", "state": "s"})

        self.assertEqual(r.status_code, 302)
        user = User.objects.get(email="bob@example.com")
        self.assertFalse(user.is_active)

    def test_callback_logs_in_active_user(self):
        User.objects.create_user(
            email="carol@example.com",
            password="x",
            is_active=True,
        )
        session = self.client.session
        session["solvro_oauth_state"] = "s"
        session["solvro_oauth_next"] = "/admin/"
        session.save()

        with (
            patch("users.views.requests.post") as p_post,
            patch("users.views.requests.get") as p_get,
        ):
            p_post.return_value.json.return_value = {"access_token": "tok"}
            p_post.return_value.raise_for_status.return_value = None
            p_get.return_value.json.return_value = {"email": "carol@example.com"}
            p_get.return_value.raise_for_status.return_value = None

            r = self.client.get(reverse("solvro_callback"), {"code": "x", "state": "s"})
        self.assertRedirects(r, "/admin/", fetch_redirect_response=False)
