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
    first_name = getattr(reset_password_token.user, 'first_name', '') or ''
    greet_suffix = f" {first_name}" if first_name else ''
    site_url = frontend_base.rstrip('/')
    # Le logo doit être dans le dossier public pour être accessible
    logo_url = getattr(settings, 'EMAIL_LOGO_URL', None) or f"{site_url}/Logo_Fr.png"
    brand = "#4F46E5"

    html_content = f"""
    <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"100%\" style=\"background:#f9fafb;padding:24px 0;\">
      <tr>
        <td align=\"center\">
          <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"600\" style=\"width:100%;max-width:600px;background:#ffffff;border-radius:12px;border:1px solid #e5e7eb;\">
            <tr>
              <td style=\"padding:24px 24px 8px;font-family:Inter,Arial,sans-serif;color:#111827;\">
                <h1 style=\"margin:0 0 8px;font-size:20px;\">Réinitialisation du mot de passe</h1>
                <p style=\"margin:0 0 16px;color:#374151;\">Bonjour{greet_suffix},</p>
                <p style=\"margin:0 0 16px;color:#374151;\">Nous avons reçu une demande de réinitialisation de votre mot de passe sur <strong>OptiTAB</strong>.</p>
                <p style=\"margin:24px 0;\">
                  <a href=\"{reset_url}\" style=\"
                      display:inline-block;background:{brand};color:#ffffff;text-decoration:none;
                      padding:12px 18px;border-radius:8px;font-weight:600\">
                    Cliquez ici pour choisir un nouveau mot de passe
                  </a>
                </p>
                <p style=\"margin:0 0 10px;color:#6b7280;\">Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur :</p>
                <p style=\"word-break:break-all;margin:0 0 16px;\"><a href=\"{reset_url}\" style=\"color:{brand};text-decoration:none;\">{reset_url}</a></p>
                <p style=\"margin:0;color:#9ca3af;font-size:12px;\">Ce lien est valable une seule fois et expirera dans 24 heures.</p>
              </td>
            </tr>
            <tr>
              <td style=\"padding:16px 24px;background:#f9fafb;border-top:1px solid #e5e7eb;\">
                <table role=\"presentation\" cellpadding=\"0\" cellspacing=\"0\" border=\"0\" width=\"100%\">
                  <tr>
                    <td style=\"width:120px;vertical-align:middle;\">
                      <a href=\"{site_url}\" style=\"text-decoration:none;\">
                        <img src=\"{logo_url}\" alt=\"OptiTAB\" height=\"120\" style=\"display:block;border:0;outline:none;\" />
                      </a>
                    </td>
                    <td style=\"vertical-align:middle;text-align:right;\">
                      <p style=\"margin:0 0 4px;font-family:Inter,Arial,sans-serif;color:#10257f;font-weight:600;\">OptiTAB</p>
                      <p style=\"margin:0;color:#6b7280;font-family:Inter,Arial,sans-serif;font-size:13px;\">Plateforme éducative</p>
                      <p style=\"margin:4px 0 0;color:#6b7280;font-family:Inter,Arial,sans-serif;font-size:13px;\">
                        <a href=\"mailto:contact@optitab.net\" style=\"color:{brand};text-decoration:none;\">contact@optitab.net</a> • 
                        <a href=\"{site_url}\" style=\"color:{brand};text-decoration:none;\">www.optitab.net</a>
                      </p>
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
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
