"""Page de retour d'un achat sans connexion (GuestCheckoutStatusView).

L'email saisi sur la page Stripe n'est pas vérifié : payer avec l'adresse d'un
autre ne doit JAMAIS ouvrir son compte. Seul un compte créé par l'achat lui-même
est connecté automatiquement, une seule fois.
"""
from __future__ import annotations

import time
from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from subscriptions.stripe_client import stripe

URL = "/api/subscriptions/guest-checkout/status/"
User = get_user_model()


def _session(email, *, guest=True, status="complete", payment_status="paid", created=None, sid="cs_test_guest"):
    metadata = {"plan_id": "1", "plan_mode": "one_time", "niveau_pays_id": ""}
    if guest:
        metadata["guest_checkout"] = "true"
    return stripe.checkout.Session.construct_from(
        {
            "id": sid,
            "object": "checkout.session",
            "status": status,
            "payment_status": payment_status,
            "amount_total": 399,
            "currency": "eur",
            "created": int(created if created is not None else time.time()),
            "customer": "cus_guest",
            "customer_details": {"email": email, "name": "Prénom Nom"},
            "metadata": metadata,
            "subscription": None,
            "payment_intent": "pi_guest",
        },
        "sk_test_factice",
    )


class GuestCheckoutStatusSecurityTests(TestCase):
    def setUp(self):
        self.client_api = APIClient()
        patches = [
            patch("subscriptions.views.handle_checkout_session_payment_completed"),
            patch("subscriptions.views.handle_checkout_session_completed"),
            patch("subscriptions.views.build_subscription_status", return_value={"has_access": True}),
            patch("subscriptions.views._send_welcome_set_password_email"),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)

    def _call(self, session):
        with patch("subscriptions.views.stripe.checkout.Session.retrieve", return_value=session):
            return self.client_api.get(URL, {"session_id": session["id"]})

    def test_existing_account_is_never_logged_in(self):
        victim = User.objects.create_user(email="victime@example.com", password="secret-123", first_name="V", last_name="V")
        response = self._call(_session("Victime@Example.com"))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["login_required"])
        self.assertNotIn("auth", data)
        self.assertNotIn("status", data)  # rien n'est révélé sur ce compte
        victim.refresh_from_db()
        self.assertIsNone(victim.stripe_customer_id or None)  # le client Stripe de l'acheteur n'y est pas rattaché

    def test_admin_account_is_never_logged_in(self):
        User.objects.create_user(email="admin@example.com", password="secret-123", first_name="A", last_name="A", is_staff=True)
        data = self._call(_session("admin@example.com")).json()
        self.assertTrue(data["login_required"])
        self.assertNotIn("auth", data)

    def test_new_account_is_logged_in_once(self):
        session = _session("nouveau@example.com")
        first = self._call(session).json()
        self.assertIn("auth", first)
        self.assertTrue(first["account_created"])
        user = User.objects.get(email="nouveau@example.com")
        self.assertFalse(user.has_usable_password())
        self.assertIsNotNone(user.last_login)
        self.assertEqual(user.stripe_customer_id, "cus_guest")

        # Rouvrir la page (historique du navigateur) ne reconnecte pas.
        second = self._call(_session("nouveau@example.com")).json()
        self.assertTrue(second["login_required"])
        self.assertNotIn("auth", second)

    def test_account_just_created_by_webhook_is_logged_in(self):
        created = time.time() - 30
        User.objects.create_user(email="webhook@example.com", password=None, first_name="W", last_name="W")
        data = self._call(_session("webhook@example.com", created=created)).json()
        self.assertIn("auth", data)

    def test_account_older_than_the_purchase_is_not_logged_in(self):
        user = User.objects.create_user(email="ancien@example.com", password=None, first_name="O", last_name="O")
        User.objects.filter(pk=user.pk).update(date_joined=timezone.now() - timedelta(days=30))
        data = self._call(_session("ancien@example.com")).json()
        self.assertTrue(data["login_required"])
        self.assertNotIn("auth", data)

    def test_old_session_does_not_log_in(self):
        created = time.time() - 3 * 3600
        user = User.objects.create_user(email="tard@example.com", password=None, first_name="T", last_name="T")
        User.objects.filter(pk=user.pk).update(date_joined=timezone.now() - timedelta(hours=3))
        data = self._call(_session("tard@example.com", created=created)).json()
        self.assertTrue(data["login_required"])

    def test_unpaid_session_creates_nothing(self):
        response = self._call(_session("impaye@example.com", status="open", payment_status="unpaid"))
        self.assertEqual(response.status_code, 202)
        self.assertTrue(response.json()["pending"])
        self.assertFalse(User.objects.filter(email="impaye@example.com").exists())

    def test_non_guest_session_is_refused(self):
        response = self._call(_session("cours@example.com", guest=False))
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(email="cours@example.com").exists())
