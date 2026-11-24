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


class VerrouillageAbonnementTests(TestCase):
    """Fin et modification d'abonnement : le verrou ne doit porter que sur la ligne
    (PostgreSQL refuse FOR UPDATE sur une jointure externe ; panne réelle du 24/11/2026)."""

    def setUp(self):
        from datetime import timedelta
        from decimal import Decimal

        from django.contrib.auth import get_user_model
        from django.utils import timezone

        from subscriptions.models import SubscriptionPlan, UserSubscription

        user = get_user_model().objects.create_user(email='verrou@example.com', password='x', first_name='V', last_name='V')
        plan = SubscriptionPlan.objects.create(
            name='Mensuel', plan_type='basic', plan_mode='subscription', billing_period='monthly',
            price=Decimal('7.99'), stripe_price_id='price_verrou', features=[],
        )
        self.fin = timezone.now() + timedelta(days=10)
        self.abonnement = UserSubscription.objects.create(
            user=user, plan=plan, status='active', stripe_subscription_id='sub_verrou',
            current_period_start=self.fin - timedelta(days=30), current_period_end=self.fin, niveau_pays=None,
        )

    def test_subscription_updated_and_deleted_are_saved(self):
        from subscriptions.handlers import handle_subscription_deleted, handle_subscription_updated

        horodatage = int(self.fin.timestamp())
        handle_subscription_updated({'id': 'sub_verrou', 'status': 'active', 'cancel_at_period_end': True,
                                     'current_period_start': horodatage - 30 * 86400, 'current_period_end': horodatage},
                                    notifier=False)
        self.abonnement.refresh_from_db()
        self.assertTrue(self.abonnement.cancel_at_period_end)
        handle_subscription_deleted({'id': 'sub_verrou', 'status': 'canceled'}, notifier=False)
        self.abonnement.refresh_from_db()
        self.assertEqual(self.abonnement.status, 'canceled')
