from __future__ import annotations

from unittest.mock import patch

from django.test import TestCase

from subscriptions.stripe_client import stripe_error


class StripeWebhookSignatureSecretsTests(TestCase):
    webhook_url = "/api/subscriptions/webhook/"

    def _build_payload(self):
        return (
            b'{"id":"evt_test_1","type":"checkout.session.completed",'
            b'"data":{"object":{"id":"cs_test_1","status":"complete","payment_status":"paid"}}}'
        )

    def _signature_error(self, message: str = "invalid signature"):
        return stripe_error.SignatureVerificationError(message, "t=123,v1=bad")

    def test_webhook_accepts_alternate_configured_secret(self):
        payload = self._build_payload()
        event = {
            "id": "evt_test_1",
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_1",
                    "status": "complete",
                    "payment_status": "paid",
                }
            },
        }

        def construct_event(_payload, _sig_header, webhook_secret):
            if webhook_secret == "whsec_primary":
                raise self._signature_error()
            if webhook_secret == "whsec_secondary":
                return event
            raise AssertionError(f"Unexpected webhook secret: {webhook_secret}")

        with patch(
            "subscriptions.views.get_stripe_webhook_secrets",
            return_value=("whsec_primary", "whsec_secondary"),
        ), patch(
            "subscriptions.views.stripe.Webhook.construct_event",
            side_effect=construct_event,
        ) as construct_event_mock, patch(
            "subscriptions.views.handle_checkout_session_payment_completed",
        ) as payment_handler_mock:
            response = self.client.post(
                self.webhook_url,
                data=payload,
                content_type="application/json",
                HTTP_STRIPE_SIGNATURE="t=123,v1=bad",
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(construct_event_mock.call_count, 2)
        payment_handler_mock.assert_called_once_with(event["data"]["object"])

    def test_webhook_returns_400_when_no_secret_matches(self):
        payload = self._build_payload()

        with patch(
            "subscriptions.views.get_stripe_webhook_secrets",
            return_value=("whsec_live", "whsec_test"),
        ), patch(
            "subscriptions.views.stripe.Webhook.construct_event",
            side_effect=self._signature_error(),
        ) as construct_event_mock:
            response = self.client.post(
                self.webhook_url,
                data=payload,
                content_type="application/json",
                HTTP_STRIPE_SIGNATURE="t=123,v1=bad",
            )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(construct_event_mock.call_count, 2)
