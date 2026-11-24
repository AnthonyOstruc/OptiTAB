"""Courriels du compte et des paiements (core/courriels.py).

Pour chaque événement : qui reçoit quoi. Les chiffres internes ne vont jamais
chez un client, et un envoi raté ne casse jamais rien.
"""
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.utils import timezone

from core import courriels
from core.services import EmailService
from pays.models import Niveau, Pays
from subscriptions.models import AccessPass, LessonPayment, PaymentHistory, SubscriptionPlan, UserSubscription

User = get_user_model()
ADMIN = 'contact@optitab.net'
STATS = {'count': 4, 'mode_label': 'LIVE', 'error_message': None}


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', FRONTEND_URL='https://www.optitab.net')
class CourrielsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        pays = Pays.objects.create(nom='France', code_iso='FRA')
        cls.niveau = Niveau.objects.create(pays=pays, nom='Terminale', ordre=12)
        cls.eleve = User.objects.create_user(email='eleve@example.com', password='x', first_name='Léa', last_name='Martin',
                                             niveau_pays=cls.niveau)
        cls.parent = User.objects.create_user(email='parent@example.com', password='x', first_name='Paul', last_name='Martin',
                                              role='parent')
        cls.mensuel = SubscriptionPlan.objects.create(
            name='Mensuel', plan_type='basic', plan_mode='subscription', billing_period='monthly',
            price=Decimal('7.99'), stripe_price_id='price_courriels_sub', features=[])
        cls.pass_jour = SubscriptionPlan.objects.create(
            name='Pass 1 jour', plan_type='basic', plan_mode='one_time', billing_period='daily',
            price=Decimal('3.99'), stripe_price_id='price_courriels_pass', features=[], access_days=1)
        cls.fin = timezone.now() + timedelta(days=30)
        cls.abonnement = UserSubscription.objects.create(
            user=cls.eleve, plan=cls.mensuel, status='active', stripe_subscription_id='sub_courriels',
            current_period_start=timezone.now(), current_period_end=cls.fin, niveau_pays=cls.niveau)
        cls.paiement = PaymentHistory.objects.create(
            user=cls.eleve, stripe_payment_intent_id='pi_courriels', amount=Decimal('7.99'), status='succeeded',
            plan_name='Mensuel', plan_mode='subscription', period_end=cls.fin, niveau_pays=cls.niveau)

    def setUp(self):
        mail.outbox.clear()
        for cible, valeur in (('core.courriels.mode_test', False),):
            p = patch(cible, return_value=valeur)
            p.start()
            self.addCleanup(p.stop)
        p = patch.object(EmailService, '_count_active_subscriptions_on_stripe', return_value=STATS)
        p.start()
        self.addCleanup(p.stop)

    def _recus(self):
        return {m.to[0]: m for m in mail.outbox}

    def _html(self, message):
        return message.alternatives[0][0]

    # ---------------------------------------------------------------- habillage
    def test_layout_is_shared_and_escapes_user_text(self):
        pirate = User.objects.create_user(email='x@example.com', password='x', first_name='<script>alert(1)</script>', last_name='')
        mail.outbox.clear()
        self.assertTrue(courriels.bienvenue(pirate))
        html = self._html(mail.outbox[0])
        self.assertNotIn('<script>', html)
        self.assertIn('&lt;script&gt;', html)
        self.assertIn('logo-optitab.png', html)
        self.assertIn('Ouvrir mon espace', html)
        self.assertIn('Ouvrir mon espace : https://www.optitab.net/dashboard', mail.outbox[0].body)

    def test_test_mode_marks_the_subject(self):
        with patch('core.courriels.mode_test', return_value=True):
            courriels.bienvenue(self.eleve)
        self.assertTrue(mail.outbox[0].subject.startswith('[TEST] '))
        mail.outbox.clear()
        courriels.bienvenue(self.eleve)
        self.assertEqual(mail.outbox[0].subject, 'Bienvenue sur OptiTAB')

    def test_a_failed_send_never_raises(self):
        with patch('core.courriels.EmailMultiAlternatives.send', side_effect=OSError('SMTP en panne')):
            self.assertFalse(courriels.achat(self.eleve, self.mensuel, self.niveau))
            self.assertFalse(courriels.paiement_refuse(self.abonnement, {'amount_due': 799}))

    # ---------------------------------------------------------------- compte
    def test_new_account_alerts_the_administration(self):
        with self.captureOnCommitCallbacks(execute=True):
            User.objects.create_user(email='nouveau@example.com', password='x', first_name='Noé', last_name='Petit',
                                     niveau_pays=self.niveau)
        message = self._recus()[ADMIN]
        self.assertEqual(message.subject, '[OptiTAB] Nouveau compte : Noé Petit')
        self.assertIn('nouveau@example.com', message.body)
        self.assertIn('Classe : Terminale · France', message.body)

    def test_account_emails_go_to_the_right_address(self):
        courriels.verification_adresse(self.eleve, 'https://exemple/verif')
        courriels.changement_adresse(self.eleve, 'nouvelle@example.com', 'https://exemple/changer')
        courriels.mot_de_passe_oublie(self.eleve, 'https://exemple/mdp')
        courriels.bienvenue_apres_achat(self.eleve, 'https://exemple/choisir')
        courriels.compte_enfant_cree(self.eleve, 'Provisoire-1', self.parent)
        self.assertEqual([m.to[0] for m in mail.outbox],
                         ['eleve@example.com', 'nouvelle@example.com', 'eleve@example.com', 'eleve@example.com', 'eleve@example.com'])
        self.assertIn('https://exemple/verif', self._html(mail.outbox[0]))
        self.assertIn('Provisoire-1', mail.outbox[4].body)

    # ---------------------------------------------------------------- achats
    def test_customer_emails_never_show_internal_figures(self):
        courriels.achat(self.eleve, self.mensuel, self.niveau, 'https://exemple/facture')
        courriels.achat(self.eleve, self.pass_jour, self.niveau)
        courriels.renouvellement(self.eleve, self.mensuel, self.niveau, 'https://exemple/facture', self.paiement)
        courriels.resiliation(self.eleve, self.mensuel, self.niveau, self.fin, True)
        courriels.cadeau_recu(self.eleve, self.parent, self.mensuel, self.niveau)
        courriels.cadeau_confirme(self.parent, self.eleve, self.mensuel, self.niveau)
        self.assertEqual(len(mail.outbox), 6)
        for message in mail.outbox:
            for interdit in ('Abonnements actifs', 'Passes actifs', 'Mode Stripe'):
                self.assertNotIn(interdit, message.body)
                self.assertNotIn(interdit, self._html(message))
        self.assertEqual(mail.outbox[0].subject, 'Ton abonnement OptiTAB est activé')
        self.assertIn('Montant : 7,99 € par mois', mail.outbox[0].body)
        self.assertEqual(mail.outbox[1].subject, 'Ton pass OptiTAB est activé')
        self.assertIn('Durée : 1 jour', mail.outbox[1].body)

    def test_admin_purchase_email_shows_figures_and_gift(self):
        EmailService.send_new_subscription_notification_to_admin(self.eleve, self.mensuel, self.niveau, is_gift=True, payer=self.parent)
        EmailService.send_new_subscription_notification_to_admin(self.eleve, self.pass_jour, self.niveau)
        cadeau, un_pass = mail.outbox
        self.assertEqual(cadeau.to, [ADMIN])
        self.assertEqual(cadeau.subject, '[OptiTAB] Nouvel abonnement : Léa Martin – Mensuel')
        for attendu in ('Abonnements actifs Stripe : 4', 'Passes actifs : 0', 'Mode Stripe : LIVE',
                        'Cadeau offert par : Paul Martin (parent@example.com)'):
            self.assertIn(attendu, cadeau.body)
        self.assertIn('Abonnements actifs Stripe', self._html(cadeau))
        self.assertEqual(un_pass.subject, '[OptiTAB] Achat de pass : Léa Martin – Pass 1 jour')

    def test_admin_email_survives_a_stripe_outage(self):
        panne = {'count': None, 'mode_label': 'LIVE', 'error_message': 'stripe down'}
        acces = AccessPass.objects.create(user=self.eleve, plan=self.pass_jour, starts_at=timezone.now() - timedelta(days=2),
                                          ends_at=timezone.now() - timedelta(days=1), stripe_payment_intent_id='pi_expire')
        with patch.object(EmailService, '_count_active_subscriptions_on_stripe', return_value=panne):
            self.assertTrue(EmailService.send_pass_expiration_notification_to_admin(self.eleve, acces, self.niveau))
        self.assertIn('Abonnements actifs Stripe : Indisponible', mail.outbox[0].body)
        self.assertIn('Erreur Stripe : stripe down', mail.outbox[0].body)

    # ---------------------------------------------------------------- événements à deux destinataires
    def test_each_event_reaches_the_customer_and_the_administration(self):
        versement = LessonPayment.objects.create(amount=Decimal('20.00'), label='Cours du lundi', payer_name='Paul Martin',
                                                 payer_email='parent@example.com', status='paid', stripe_session_id='cs_courriels',
                                                 paid_at=timezone.now())
        evenements = {
            'carte refusée': (lambda: courriels.paiement_refuse(
                self.abonnement, {'amount_due': 799, 'customer_email': 'parent@example.com', 'hosted_invoice_url': 'https://exemple/regler'}),
                'parent@example.com', 'Ton paiement OptiTAB n’est pas passé', 'Carte refusée'),
            'réactivation': (lambda: courriels.reactivation(self.eleve, self.abonnement),
                             'eleve@example.com', 'Ton abonnement OptiTAB continue', 'Réactivation'),
            'changement': (lambda: courriels.changement_offre(self.eleve, self.mensuel, self.pass_jour, self.niveau, self.fin),
                           'eleve@example.com', 'Ton abonnement OptiTAB a changé', 'Changement d’offre'),
            'remboursement': (lambda: courriels.remboursement(self.eleve, 7.99, 'Mensuel', total=True, acces_ferme=True),
                              'eleve@example.com', 'Ton remboursement OptiTAB', 'Remboursement'),
            'doublon': (lambda: courriels.achat_en_double(self.eleve, self.mensuel, self.niveau, 'pi_double'),
                        'eleve@example.com', 'Ton paiement en double a été remboursé', 'Achat en double remboursé'),
        }
        for nom, (declencher, client, sujet_client, sujet_admin) in evenements.items():
            mail.outbox.clear()
            self.assertTrue(declencher(), nom)
            recus = self._recus()
            self.assertEqual(set(recus), {client, ADMIN}, nom)
            self.assertEqual(recus[client].subject, sujet_client, nom)
            self.assertTrue(recus[ADMIN].subject.startswith(f'[OptiTAB] {sujet_admin}'), recus[ADMIN].subject)

        mail.outbox.clear()
        courriels.resiliation(self.eleve, self.mensuel, self.niveau, self.fin, False)
        courriels.resiliation_admin(self.eleve, self.mensuel, self.niveau, self.fin, False)
        courriels.renouvellement_admin(self.eleve, self.mensuel, self.niveau, self.paiement)
        courriels.litige(7.99, 'fraudulent', 'dp_1', self.eleve)
        courriels.versement_cours(versement)
        courriels.message_stripe_non_traite('invoice.paid', 'evt_1', 'base indisponible')
        self.assertEqual([m.subject for m in mail.outbox], [
            'Ton abonnement OptiTAB est terminé',
            '[OptiTAB] Abonnement terminé : Léa Martin – Mensuel',
            '[OptiTAB] Renouvellement : Léa Martin – Mensuel',
            '[OptiTAB] Litige bancaire : 7,99 €',
            '[OptiTAB] Versement reçu (cours particulier) : 20,00 €',
            '[OptiTAB] Message Stripe non traité : invoice.paid',
        ])
        self.assertEqual([m.to[0] for m in mail.outbox], ['eleve@example.com'] + [ADMIN] * 5)
