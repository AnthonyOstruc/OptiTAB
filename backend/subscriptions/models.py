from django.db import models
from django.conf import settings
from django.utils import timezone
import logging
from .stripe_client import stripe, stripe_error
from .helpers import _from_timestamp
from pays.models import Niveau

logger = logging.getLogger(__name__)


def _user_identifier(user):
    """Return a display-safe identifier for the custom user model."""
    if not user:
        return 'Utilisateur'
    if hasattr(user, 'get_username'):
        username = user.get_username()
        if username:
            return username
    email = getattr(user, 'email', None)
    if email:
        return email
    return getattr(user, 'id', 'Utilisateur')

class SubscriptionPlan(models.Model):
    """Plans d'abonnement disponibles"""
    # `unique_together` porte sur (plan_type, billing_period, plan_mode) :
    # deux offres mensuelles recurrentes doivent donc avoir des types
    # differents. D'ou ces types metier plutot qu'un simple basic/premium.
    PLAN_TYPES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('accompagne', 'Accompagne (questions illimitees)'),
        ('particuliers', 'Cours particuliers'),
    ]
    
    BILLING_PERIODS = [
        ('daily', 'Journalier'),
        ('weekly', 'Hebdomadaire'),
        ('monthly', 'Mensuel'),
        ('yearly', 'Annuel'),
    ]
    MODE_CHOICES = [
        ('subscription', 'Abonnement récurrent'),
        ('one_time', 'Pass unique'),
    ]
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    plan_mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='subscription', db_index=True)
    billing_period = models.CharField(max_length=20, choices=BILLING_PERIODS)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_price_id = models.CharField(max_length=100, unique=True)
    stripe_price_id_test = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        help_text="Price ID Stripe en mode test (utilisé en local/dev).",
    )
    features = models.JSONField(default=list)  # Liste des fonctionnalités
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    access_days = models.PositiveIntegerField(null=True, blank=True, help_text="Pour les passes one-time: nombre de jours d'accès")
    
    class Meta:
        unique_together = ['plan_type', 'billing_period', 'plan_mode']
    
    def __str__(self):
        return f"{self.name} - {self.get_billing_period_display()}"


class AccessPass(models.Model):
    """Accès temporaire via paiement one-time (ex: 1 jour, 1 mois)"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='access_passes')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, limit_choices_to={'plan_mode': 'one_time'})
    starts_at = models.DateTimeField(default=timezone.now)
    ends_at = models.DateTimeField()
    stripe_payment_intent_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_email_sent = models.BooleanField(default=False)
    is_revoked = models.BooleanField(default=False, help_text="Pass révoqué suite à un remboursement")
    revoked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'ends_at']),
        ]

    def __str__(self):
        return f"Pass {self.plan.name} → {self.user} jusqu'au {self.ends_at.isoformat()}"

    @property
    def is_active(self):
        """Le pass est actif s'il n'est pas expiré et n'a pas été révoqué."""
        if self.is_revoked:
            return False
        return timezone.now() < self.ends_at
    
    def revoke(self):
        """Révoque le pass (utilisé lors d'un remboursement)."""
        self.is_revoked = True
        self.revoked_at = timezone.now()
        self.save(update_fields=['is_revoked', 'revoked_at'])

class UserSubscription(models.Model):
    """Abonnement d'un utilisateur"""
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('trialing', 'Essai gratuit'),
        ('past_due', 'Impayé'),
        ('canceled', 'Annulé'),
        ('unpaid', 'Non payé'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=100, null=True, blank=True)
    niveau_pays = models.ForeignKey(
        Niveau,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='subscriptions'
    )
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trialing')
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    cancel_at_period_end = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{_user_identifier(self.user)} - {self.plan.name} ({self.status})"
    
    @property
    def is_active(self):
        """Vérifie si l'abonnement donne toujours accès."""
        if self.status in ['active', 'trialing']:
            return True
        if self.cancel_at_period_end and self.current_period_end:
            if self.current_period_end > timezone.now():
                return True
        return False
    
    @property
    def is_trial(self):
        """Vérifie si l'utilisateur est en période d'essai"""
        return self.status == 'trialing' and self.trial_end and timezone.now() < self.trial_end
    
    @property
    def days_remaining_trial(self):
        """Nombre de jours restants dans l'essai gratuit"""
        if self.is_trial:
            return (self.trial_end - timezone.now()).days
        return 0
    
    def cancel_subscription(self):
        """Planifie l'annulation à la fin de la période de facturation."""
        if self.cancel_at_period_end and self.current_period_end and self.current_period_end > timezone.now():
            return True
        if not self.stripe_subscription_id:
            self.status = 'canceled'
            self.cancel_at_period_end = False
            self.save(update_fields=['status', 'cancel_at_period_end'])
            return True

        try:
            stripe.Subscription.modify(
                self.stripe_subscription_id,
                cancel_at_period_end=True
            )
            updated = stripe.Subscription.retrieve(self.stripe_subscription_id)
            if hasattr(updated, 'to_dict'):
                updated = updated.to_dict()
            self.status = updated.get('status', self.status)
            self.current_period_start = _from_timestamp(updated.get('current_period_start')) or self.current_period_start
            self.current_period_end = _from_timestamp(updated.get('current_period_end')) or self.current_period_end
            self.trial_end = _from_timestamp(updated.get('trial_end')) or self.trial_end
            self.cancel_at_period_end = bool(updated.get('cancel_at_period_end', True))
            self.save(update_fields=['status', 'current_period_start', 'current_period_end', 'trial_end', 'cancel_at_period_end', 'updated_at'])
            return True
        except stripe_error.InvalidRequestError as exc:
            logger.warning(f"Stripe indique que l'abonnement {self.stripe_subscription_id} est déjà annulé ou introuvable: {exc}")
            self.status = 'canceled'
            self.cancel_at_period_end = False
            self.save(update_fields=['status', 'cancel_at_period_end', 'updated_at'])
            return True
        except stripe_error.StripeError as e:
            logger.error(f"Erreur lors de l'annulation: {e}")
            return False

class PaymentHistory(models.Model):
    """Historique des paiements"""
    PLAN_MODE_CHOICES = [
        ('subscription', 'Abonnement récurrent'),
        ('one_time', 'Pass ponctuel'),
        ('payment', 'Paiement simple'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    stripe_payment_intent_id = models.CharField(max_length=100, unique=True)
    stripe_invoice_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    hosted_invoice_url = models.URLField(blank=True, default='')
    invoice_pdf_url = models.URLField(blank=True, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='EUR')
    status = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    plan_name = models.CharField(max_length=255, blank=True, default='')
    plan_mode = models.CharField(max_length=20, choices=PLAN_MODE_CHOICES, default='payment')
    period_start = models.DateTimeField(null=True, blank=True)
    period_end = models.DateTimeField(null=True, blank=True)
    niveau_pays = models.ForeignKey(
        Niveau,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payment_history_entries'
    )
    niveau_label = models.CharField(max_length=255, blank=True, default='')
    email_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        level_info = f" · {self.niveau_label}" if self.niveau_label else ''
        return f"{_user_identifier(self.user)} - {self.amount}€ ({self.status}){level_info}"
