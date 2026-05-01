from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from applications.models import Application

from .models import Alert


class AlertEndpointTests(TestCase):
    def setUp(self):
        self.list_url = reverse("alert-list")
        self.testownik = Application.objects.create(name="Testownik")
        self.planer = Application.objects.create(name="Planer")

    def _make(self, **overrides):
        kwargs = {
            "title": "T",
            "content": "<p>hi</p>",
            "is_active": True,
            "is_global": False,
        }
        kwargs.update(overrides)
        return Alert.objects.create(**kwargs)

    def test_endpoint_is_public(self):
        self.assertEqual(self.client.get(self.list_url).status_code, 200)

    def test_no_app_param_returns_only_global(self):
        global_alert = self._make(is_global=True)
        scoped = self._make()
        scoped.applications.add(self.testownik)

        ids = {a["id"] for a in self.client.get(self.list_url).json()}
        self.assertEqual(ids, {str(global_alert.id)})

    def test_app_param_includes_global_and_targeted(self):
        global_alert = self._make(is_global=True)
        scoped = self._make()
        scoped.applications.add(self.testownik)
        other = self._make()
        other.applications.add(self.planer)

        ids = {
            a["id"] for a in self.client.get(self.list_url, {"app": "testownik"}).json()
        }
        self.assertEqual(ids, {str(global_alert.id), str(scoped.id)})
        self.assertNotIn(str(other.id), ids)

    def test_inactive_alerts_excluded(self):
        self._make(is_global=True, is_active=False)
        self.assertEqual(self.client.get(self.list_url).json(), [])

    def test_expired_alerts_excluded(self):
        now = timezone.now()
        self._make(is_global=True, end_at=now - timedelta(minutes=1))
        self._make(is_global=True, start_at=now + timedelta(minutes=1))

        self.assertEqual(self.client.get(self.list_url).json(), [])

    def test_unknown_app_returns_400(self):
        r = self.client.get(self.list_url, {"app": "ghost"})
        self.assertEqual(r.status_code, 400)
        self.assertIn("app", r.json())

    def test_active_window_alerts_returned(self):
        now = timezone.now()
        live = self._make(
            is_global=True,
            start_at=now - timedelta(minutes=1),
            end_at=now + timedelta(minutes=10),
        )
        ids = [a["id"] for a in self.client.get(self.list_url).json()]
        self.assertIn(str(live.id), ids)


class AlertModelTests(TestCase):
    def test_save_strips_dangerous_html(self):
        alert = Alert.objects.create(
            title="x",
            content="<p>ok</p><script>alert(1)</script><img src=x onerror=alert(1)>",
            is_global=True,
        )
        self.assertNotIn("<script>", alert.content)
        self.assertNotIn("<img", alert.content)
        self.assertIn("ok", alert.content)
