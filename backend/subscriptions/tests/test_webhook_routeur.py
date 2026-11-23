"""Aiguillage des webhooks Stripe (views._handle_webhook_event)."""
from unittest.mock import patch

from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings

from subscriptions import views


def _evenement(type_, objet=None):
    return {'id': 'evt_routeur', 'type': type_, 'data': {'object': objet or {'id': 'in_routeur', 'object': 'invoice'}}}


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class RouteurWebhookTests(TestCase):
    def setUp(self):
        cache.clear()

    def test_unknown_event_is_acknowledged(self):
        self.assertEqual(views._handle_webhook_event(_evenement('customer.created')).status_code, 200)

    def test_invoice_paid_is_routed_with_fresh_object(self):
        frais = {'id': 'in_routeur', 'object': 'invoice', 'subscription': 'sub_routeur'}
        with patch.dict(views.GESTIONNAIRES_WEBHOOK, {'invoice.paid': lambda o: self.assertEqual(o, frais)}), \
                patch.object(views, '_objet_a_jour', return_value=frais) as relire:
            reponse = views._handle_webhook_event(_evenement('invoice.paid'))
        self.assertEqual(reponse.status_code, 200)
        relire.assert_called_once()

    def test_failure_returns_500_and_alerts_once(self):
        def echec(_objet):
            raise RuntimeError('base indisponible')

        with patch.dict(views.GESTIONNAIRES_WEBHOOK, {'invoice.paid': echec}), \
                patch.object(views, '_objet_a_jour', side_effect=lambda o: o):
            premiere = views._handle_webhook_event(_evenement('invoice.paid'))
            seconde = views._handle_webhook_event(_evenement('invoice.paid'))
        self.assertEqual((premiere.status_code, seconde.status_code), (500, 500))
        self.assertEqual(len(mail.outbox), 1)  # une alerte par type et par heure
        self.assertIn('non traité', mail.outbox[0].subject)

    def test_fresh_object_falls_back_to_payload_when_missing(self):
        objet = {'id': 'sub_supprime', 'object': 'subscription', 'status': 'canceled'}
        erreur = views.stripe_error.InvalidRequestError('No such subscription', 'id')
        with patch.object(views.stripe.Subscription, 'retrieve', side_effect=erreur):
            self.assertEqual(views._objet_a_jour(objet), objet)

    def test_test_webhook_is_closed_in_production(self):
        with patch.object(views, '_is_stripe_test_runtime', return_value=False):
            reponse = self.client.post('/api/subscriptions/webhook/test/', data='{}', content_type='application/json')
        self.assertEqual(reponse.status_code, 404)
