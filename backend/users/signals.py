import logging

from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created

from core import courriels

logger = logging.getLogger(__name__)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """Mot de passe oublié : lien pour en choisir un nouveau."""
    frontend_base = getattr(settings, 'FRONTEND_BASE_URL', getattr(settings, 'FRONTEND_URL', 'http://localhost:3000'))
    lien = f"{frontend_base.rstrip('/')}/password-reset?token={reset_password_token.key}"
    courriels.mot_de_passe_oublie(reset_password_token.user, lien)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def prevenir_nouveau_compte(sender, instance, created, raw=False, **kwargs):
    """Chaque compte créé (inscription, Google, achat sans connexion, compte enfant)
    est signalé à l'administration, une fois l'enregistrement validé."""
    if created and not raw:
        transaction.on_commit(lambda: courriels.nouveau_compte_admin(instance))
