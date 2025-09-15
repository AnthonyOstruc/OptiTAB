from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    frontend_base = getattr(settings, 'FRONTEND_BASE_URL', getattr(settings, 'FRONTEND_URL', 'http://localhost:3000'))
    reset_url = f"{frontend_base.rstrip('/')}/password-reset?token={reset_password_token.key}"
    message = f"Bonjour,\n\nCliquez sur le lien suivant pour réinitialiser votre mot de passe :\n\n{reset_url}\n\nMerci."

    # Version HTML professionnelle
    html_content = f"""
    <div style=\"font-family:Inter,Arial,sans-serif;line-height:1.6;color:#111827\">
      <p>Bonjour,</p>
      <p>Vous avez demandé à réinitialiser votre mot de passe sur <strong>OptiTAB</strong>.</p>
      <p style=\"margin:24px 0\">
        <a href=\"{reset_url}\" style=\"
            display:inline-block;background:#4F46E5;color:#ffffff;text-decoration:none;
            padding:12px 18px;border-radius:8px;font-weight:600\">
          Cliquez ici pour choisir un nouveau mot de passe
        </a>
      </p>
      <p>Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur :</p>
      <p style=\"word-break:break-all;color:#4F46E5\">{reset_url}</p>
      <hr style=\"border:none;border-top:1px solid #e5e7eb;margin:24px 0\" />
      <p style=\"margin:0\"><strong>OptiTAB</strong></p>
      <p style=\"margin:0;color:#6b7280\">Plateforme éducative</p>
      <p style=\"margin:0;color:#6b7280\"><a href=\"https://optitab.net\" style=\"color:#4F46E5;text-decoration:none\">optitab.net</a></p>
      <p style=\"margin:0;color:#6b7280\">contact@optitab.net</p>
    </div>
    """

    # Ne jamais faire échouer la requête si l'envoi d'email tombe en erreur
    email_host = getattr(settings, 'EMAIL_HOST', None)
    email_user = getattr(settings, 'EMAIL_HOST_USER', None)
    if not email_host or not email_user:
        logger.warning(
            "Password reset email not sent: email backend not fully configured (EMAIL_HOST/EMAIL_HOST_USER missing)."
        )
        return

    try:
        # Envoi multipart (texte + HTML)
        subject = "Réinitialisation de votre mot de passe - OptiTAB"
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [reset_password_token.user.email]

        email = EmailMultiAlternatives(subject, message, from_email, to)
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
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
