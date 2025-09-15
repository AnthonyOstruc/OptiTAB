from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    frontend_base = getattr(settings, 'FRONTEND_BASE_URL', getattr(settings, 'FRONTEND_URL', 'http://localhost:3000'))
    reset_url = f"{frontend_base.rstrip('/')}/password-reset?token={reset_password_token.key}"
    message = f"Bonjour,\n\nCliquez sur le lien suivant pour réinitialiser votre mot de passe :\n\n{reset_url}\n\nMerci."

    # Ne jamais faire échouer la requête si l'envoi d'email tombe en erreur
    email_host = getattr(settings, 'EMAIL_HOST', None)
    email_user = getattr(settings, 'EMAIL_HOST_USER', None)
    if not email_host or not email_user:
        logger.warning(
            "Password reset email not sent: email backend not fully configured (EMAIL_HOST/EMAIL_HOST_USER missing)."
        )
        return

    try:
        send_mail(
            subject="Réinitialisation de votre mot de passe - OptiTAB",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reset_password_token.user.email],
            fail_silently=False,
        )
    except Exception as exc:
        # Journaliser l'erreur sans exposer le token ni renvoyer une 500
        logger.error(
            "Failed to send password reset email to user_id=%s email=%s: %s",
            getattr(reset_password_token.user, 'id', 'unknown'),
            getattr(reset_password_token.user, 'email', 'unknown'),
            str(exc),
            exc_info=True,
        )
        # Ne pas relancer l'exception pour éviter une 500 côté API
        return
