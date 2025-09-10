from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import logging
import stripe
from stripe_config import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)

class SubscriptionPlan(models.Model):
    """Plans d'abonnement disponibles"""
    PLAN_TYPES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
    ]
    
    BILLING_PERIODS = [
        ('monthly', 'Mensuel'),
        ('yearly', 'Annuel'),
    ]
    
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    billing_period = models.CharField(max_length=20, choices=BILLING_PERIODS)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_price_id = models.CharField(max_length=100, unique=True)
    features = models.JSONField(default=list)  # Liste des fonctionnalités
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['plan_type', 'billing_period']
    
    def __str__(self):
        return f"{self.name} - {self.get_billing_period_display()}"

class UserSubscription(models.Model):
    """Abonnement d'un utilisateur"""
    STATUS_CHOICES = [
        ('active', 'Actif'),
        ('trialing', 'Essai gratuit'),
        ('past_due', 'Impayé'),
        ('canceled', 'Annulé'),
        ('unpaid', 'Non payé'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=100, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trialing')
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    trial_end = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name} ({self.status})"
    
    @property
    def is_active(self):
        """Vérifie si l'abonnement est actif"""
        return self.status in ['active', 'trialing']
    
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
        """Annule l'abonnement Stripe"""
        if self.stripe_subscription_id:
            try:
                stripe.Subscription.delete(self.stripe_subscription_id)
                self.status = 'canceled'
                self.save()
                return True
            except stripe.error.StripeError as e:
                logger.error(f"Erreur lors de l'annulation: {e}")
                return False
        return False

class PaymentHistory(models.Model):
    """Historique des paiements"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    stripe_payment_intent_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='EUR')
    status = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.amount}€ ({self.status})"
