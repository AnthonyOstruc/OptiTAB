"""Tests pour la landing /diagnostic-maths-gratuit.

Couvre :
  - L'endpoint POST /api/newsletter/diagnostic-lead/
  - Le modèle DiagnosticLead
  - L'action admin export CSV
"""
from datetime import timedelta
from unittest.mock import patch

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from core.admin import DiagnosticLeadAdmin
from core.models import DiagnosticLead, NewsletterSubscriber


VALID_PAYLOAD = {
    "firstName": "Léa",
    "email": "lea@example.fr",
    "level": "terminale",
    "difficulty": "cours_vs_exercices",
    "consentEmailMarketing": True,
    "formLocation": "main",
    "leadMagnet": "diagnostic_maths",
    "context": {
        "utm_source": "google",
        "utm_medium": "cpc",
        "utm_campaign": "diagnostic_v1",
        "utm_content": "ad_a",
        "utm_term": "diagnostic maths",
        "gclid": "abc123",
        "fbclid": "",
        "ttclid": "",
        "msclkid": "",
        "referrer": "https://www.google.com/",
        "landing_path": "/diagnostic-maths-gratuit",
    },
}


@override_settings(ALLOWED_HOSTS=['testserver', 'localhost', '127.0.0.1'])
class DiagnosticLeadEndpointTests(TestCase):
    """Tests fonctionnels pour POST /api/newsletter/diagnostic-lead/."""

    def setUp(self):
        self.client = APIClient(HTTP_ACCEPT='application/json')
        self.url = reverse('core:diagnostic_lead')

    def _post(self, payload, **extra):
        return self.client.post(
            self.url,
            payload,
            format='json',
            HTTP_ACCEPT='application/json',
            **extra,
        )

    # ---------- Cas nominal ----------

    @patch('core.newsletter_views.EmailService.send_newsletter_welcome', return_value=True)
    def test_valid_submission_with_consent_creates_lead_and_subscriber(self, mock_send):
        response = self._post(VALID_PAYLOAD)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertTrue(body['success'])
        self.assertIn('lead_id', body['data'])
        self.assertTrue(body['data']['newsletter_subscribed'])

        # Lead bien créé avec tous les champs
        lead = DiagnosticLead.objects.get(pk=body['data']['lead_id'])
        self.assertEqual(lead.email, 'lea@example.fr')
        self.assertEqual(lead.first_name, 'Léa')
        self.assertEqual(lead.level, 'terminale')
        self.assertEqual(lead.difficulty, 'cours_vs_exercices')
        self.assertTrue(lead.consent_email_marketing)
        self.assertIsNotNone(lead.consent_timestamp)
        self.assertEqual(lead.utm_source, 'google')
        self.assertEqual(lead.gclid, 'abc123')
        self.assertEqual(lead.landing_path, '/diagnostic-maths-gratuit')

        # NewsletterSubscriber créé et lié
        self.assertIsNotNone(lead.linked_subscriber_id)
        sub = NewsletterSubscriber.objects.get(email='lea@example.fr')
        self.assertEqual(sub.source, 'diagnostic_landing')
        self.assertTrue(sub.est_actif)

        # Email de bienvenue tenté
        mock_send.assert_called_once()

    def test_valid_submission_without_consent_creates_lead_no_subscriber(self):
        payload = {**VALID_PAYLOAD, 'consentEmailMarketing': False}
        response = self._post(payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        body = response.json()
        self.assertFalse(body['data']['newsletter_subscribed'])

        lead = DiagnosticLead.objects.get(pk=body['data']['lead_id'])
        self.assertFalse(lead.consent_email_marketing)
        self.assertIsNone(lead.consent_timestamp)
        self.assertIsNone(lead.linked_subscriber_id)

        # Pas de NewsletterSubscriber créé
        self.assertFalse(NewsletterSubscriber.objects.filter(email='lea@example.fr').exists())

    # ---------- Validation ----------

    def test_invalid_email_returns_400(self):
        for bad_email in ['', 'not-an-email', 'foo@', '@bar.fr', 'foo bar@baz.fr']:
            with self.subTest(email=bad_email):
                payload = {**VALID_PAYLOAD, 'email': bad_email}
                response = self._post(payload)
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn('email', response.json()['errors'])

    def test_missing_first_name_returns_400(self):
        payload = {**VALID_PAYLOAD, 'firstName': '   '}
        response = self._post(payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('firstName', response.json()['errors'])

    def test_invalid_level_returns_400(self):
        payload = {**VALID_PAYLOAD, 'level': 'cm2'}
        response = self._post(payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('level', response.json()['errors'])

    def test_invalid_difficulty_returns_400(self):
        payload = {**VALID_PAYLOAD, 'difficulty': 'flemme'}
        response = self._post(payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('difficulty', response.json()['errors'])

    def test_valid_levels_all_accepted(self):
        levels = ['college', 'seconde', 'premiere', 'terminale', 'prepa', 'bts', 'parent']
        for idx, level in enumerate(levels):
            with self.subTest(level=level):
                payload = {
                    **VALID_PAYLOAD,
                    'level': level,
                    'email': f'student{idx}@example.fr',
                    'consentEmailMarketing': False,
                }
                response = self._post(payload)
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_difficulties_all_accepted(self):
        difficulties = ['cours_vs_exercices', 'organisation', 'methode', 'bac', 'motivation']
        for idx, diff in enumerate(difficulties):
            with self.subTest(difficulty=diff):
                payload = {
                    **VALID_PAYLOAD,
                    'difficulty': diff,
                    'email': f'student-d{idx}@example.fr',
                    'consentEmailMarketing': False,
                }
                response = self._post(payload)
                self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ---------- Honeypot anti-bot ----------

    def test_honeypot_filled_does_not_create_lead(self):
        payload = {**VALID_PAYLOAD, 'website': 'http://spam.example/'}
        response = self._post(payload)
        # On simule un succès pour ne pas signaler au bot qu'il a été détecté
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DiagnosticLead.objects.count(), 0)
        self.assertEqual(NewsletterSubscriber.objects.count(), 0)

    def test_honeypot_empty_string_does_not_block(self):
        payload = {**VALID_PAYLOAD, 'website': '', 'consentEmailMarketing': False}
        response = self._post(payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DiagnosticLead.objects.count(), 1)

    # ---------- Email normalisation ----------

    def test_email_is_lowercased(self):
        payload = {**VALID_PAYLOAD, 'email': 'LEA@EXAMPLE.FR', 'consentEmailMarketing': False}
        response = self._post(payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lead = DiagnosticLead.objects.first()
        self.assertEqual(lead.email, 'lea@example.fr')

    # ---------- Multi-submission ----------

    @patch('core.newsletter_views.EmailService.send_newsletter_welcome', return_value=True)
    def test_same_email_can_submit_twice(self, mock_send):
        """Un même email peut soumettre plusieurs fois (campagnes différentes).

        Mais NewsletterSubscriber reste unique (réactivé si désinscrit)."""
        # 1ère soumission
        r1 = self._post(VALID_PAYLOAD)
        self.assertEqual(r1.status_code, status.HTTP_200_OK)

        # 2e soumission avec UTM différent
        payload2 = {
            **VALID_PAYLOAD,
            'context': {**VALID_PAYLOAD['context'], 'utm_campaign': 'retargeting'},
        }
        r2 = self._post(payload2)
        self.assertEqual(r2.status_code, status.HTTP_200_OK)

        self.assertEqual(DiagnosticLead.objects.count(), 2)
        # Un seul abonné newsletter
        self.assertEqual(NewsletterSubscriber.objects.filter(email='lea@example.fr').count(), 1)

    @patch('core.newsletter_views.EmailService.send_newsletter_welcome', return_value=True)
    def test_unsubscribed_user_resubmitting_reactivates_subscription(self, mock_send):
        # User s'inscrit puis se désabonne
        sub = NewsletterSubscriber.objects.create(
            email='lea@example.fr',
            first_name='Léa',
            est_actif=True,
            source='website',
        )
        sub.mark_unsubscribed()
        self.assertFalse(sub.est_actif)

        # Resoumission avec opt-in
        response = self._post(VALID_PAYLOAD)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        sub.refresh_from_db()
        self.assertTrue(sub.est_actif)
        self.assertIsNone(sub.unsubscribed_at)
        self.assertEqual(sub.source, 'diagnostic_landing')

    # ---------- IP capture ----------

    def test_ip_captured_from_x_forwarded_for(self):
        payload = {**VALID_PAYLOAD, 'consentEmailMarketing': False}
        response = self._post(payload, HTTP_X_FORWARDED_FOR='203.0.113.42, 10.0.0.1')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lead = DiagnosticLead.objects.first()
        self.assertEqual(lead.consent_ip, '203.0.113.42')

    # ---------- Resilience ----------

    @patch('core.newsletter_views.EmailService.send_newsletter_welcome', side_effect=Exception('SMTP down'))
    def test_email_failure_does_not_break_request(self, mock_send):
        """Si l'envoi d'email échoue, le lead doit quand même être enregistré."""
        response = self._post(VALID_PAYLOAD)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(DiagnosticLead.objects.count(), 1)
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)

    def test_long_strings_are_truncated(self):
        """Les UTM longs ne doivent pas faire planter la requête."""
        payload = {
            **VALID_PAYLOAD,
            'consentEmailMarketing': False,
            'context': {
                'utm_source': 'x' * 500,
                'gclid': 'g' * 1000,
                'referrer': 'https://example.com/' + 'a' * 1000,
                'landing_path': '/' + 'p' * 500,
            },
        }
        response = self._post(payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lead = DiagnosticLead.objects.first()
        self.assertLessEqual(len(lead.utm_source), 100)
        self.assertLessEqual(len(lead.gclid), 255)
        self.assertLessEqual(len(lead.referrer), 500)
        self.assertLessEqual(len(lead.landing_path), 255)


class DiagnosticLeadModelTests(TestCase):
    """Tests unitaires pour le modèle DiagnosticLead."""

    def test_str_representation(self):
        lead = DiagnosticLead.objects.create(
            email='test@example.fr',
            first_name='Test',
            level='seconde',
            difficulty='methode',
        )
        self.assertIn('test@example.fr', str(lead))
        self.assertIn('Seconde', str(lead))

    def test_mark_diagnostic_sent(self):
        lead = DiagnosticLead.objects.create(
            email='test@example.fr',
            first_name='Test',
            level='premiere',
            difficulty='bac',
        )
        self.assertIsNone(lead.diagnostic_sent_at)

        before = timezone.now()
        lead.mark_diagnostic_sent()
        after = timezone.now()

        lead.refresh_from_db()
        self.assertIsNotNone(lead.diagnostic_sent_at)
        self.assertGreaterEqual(lead.diagnostic_sent_at, before)
        self.assertLessEqual(lead.diagnostic_sent_at, after)

    def test_default_lead_magnet(self):
        lead = DiagnosticLead.objects.create(
            email='test@example.fr',
            first_name='Test',
            level='terminale',
            difficulty='bac',
        )
        self.assertEqual(lead.lead_magnet, 'diagnostic_maths')

    def test_default_form_location(self):
        lead = DiagnosticLead.objects.create(
            email='test@example.fr',
            first_name='Test',
            level='terminale',
            difficulty='bac',
        )
        self.assertEqual(lead.form_location, 'main')


class DiagnosticLeadAdminTests(TestCase):
    """Tests pour les actions admin (export CSV, mark as sent)."""

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.admin_user = User.objects.create_superuser(
            email='admin@optitab.net',
            password='admin-test-pwd-1234',
            first_name='Admin',
            last_name='Test',
        )
        cls.lead1 = DiagnosticLead.objects.create(
            email='alice@example.fr',
            first_name='Alice',
            level='terminale',
            difficulty='cours_vs_exercices',
            consent_email_marketing=True,
            consent_timestamp=timezone.now(),
            utm_source='google',
            utm_campaign='diagnostic_v1',
        )
        cls.lead2 = DiagnosticLead.objects.create(
            email='bob@example.fr',
            first_name='Bob',
            level='seconde',
            difficulty='methode',
            consent_email_marketing=False,
        )

    def setUp(self):
        self.factory = RequestFactory()
        self.admin = DiagnosticLeadAdmin(model=DiagnosticLead, admin_site=AdminSite())

    def _make_request(self):
        request = self.factory.get('/admin/core/diagnosticlead/')
        request.user = self.admin_user
        # Le middleware messages doit être présent pour message_user
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', {})
        setattr(request, '_messages', FallbackStorage(request))
        return request

    def test_export_as_csv_returns_csv_response(self):
        request = self._make_request()
        queryset = DiagnosticLead.objects.all()
        response = self.admin.export_as_csv(request, queryset)

        self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
        self.assertIn('attachment', response['Content-Disposition'])
        self.assertIn('diagnostic_leads_', response['Content-Disposition'])

        body = response.content.decode('utf-8-sig')
        self.assertIn('alice@example.fr', body)
        self.assertIn('bob@example.fr', body)
        self.assertIn('Alice', body)
        self.assertIn('Terminale', body)
        self.assertIn('Seconde', body)
        # Header row
        self.assertIn('utm_source', body)
        self.assertIn('consent_ip', body)

    def test_export_csv_separator_is_semicolon(self):
        request = self._make_request()
        queryset = DiagnosticLead.objects.filter(email='alice@example.fr')
        response = self.admin.export_as_csv(request, queryset)

        body = response.content.decode('utf-8-sig')
        # Le séparateur ; est utilisé (compatibilité Excel France)
        header = body.splitlines()[0]
        self.assertGreater(header.count(';'), 10)
        self.assertEqual(header.count(','), 0)

    def test_export_csv_consent_oui_non(self):
        request = self._make_request()
        queryset = DiagnosticLead.objects.all()
        response = self.admin.export_as_csv(request, queryset)

        body = response.content.decode('utf-8-sig')
        self.assertIn(';oui;', body)  # Alice a coché
        self.assertIn(';non;', body)  # Bob n'a pas coché

    def test_mark_diagnostic_sent_action(self):
        request = self._make_request()
        queryset = DiagnosticLead.objects.all()

        self.assertIsNone(self.lead1.diagnostic_sent_at)
        self.assertIsNone(self.lead2.diagnostic_sent_at)

        self.admin.mark_diagnostic_sent(request, queryset)

        self.lead1.refresh_from_db()
        self.lead2.refresh_from_db()
        self.assertIsNotNone(self.lead1.diagnostic_sent_at)
        self.assertIsNotNone(self.lead2.diagnostic_sent_at)

    def test_mark_diagnostic_sent_skips_already_sent(self):
        already_sent = timezone.now() - timedelta(days=1)
        self.lead1.diagnostic_sent_at = already_sent
        self.lead1.save(update_fields=['diagnostic_sent_at'])

        request = self._make_request()
        queryset = DiagnosticLead.objects.all()
        self.admin.mark_diagnostic_sent(request, queryset)

        self.lead1.refresh_from_db()
        # La date initiale n'a pas été écrasée
        self.assertEqual(
            self.lead1.diagnostic_sent_at.replace(microsecond=0),
            already_sent.replace(microsecond=0),
        )
