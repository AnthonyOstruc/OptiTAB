"""
Services utilitaires réutilisables pour éviter la duplication de code
"""
from django.core.mail import send_mail, EmailMultiAlternatives
import os
from django.conf import settings
from django.db import models
from rest_framework.response import Response
from rest_framework import status
import logging
import random
from email.mime.image import MIMEImage
from pathlib import Path
from django.utils import timezone

logger = logging.getLogger(__name__)


class EmailService:
    """Service centralisé pour l'envoi d'emails"""
    
    @staticmethod
    def _resolve_logo_url():
        """Retourne une URL https publique du logo si disponible.

        Priorité:
        1) EMAIL_LOGO_URL
        2) FRONTEND_URL + '/Logo_Fr.png' si FRONTEND_URL est https et non localhost
        """
        def _append_version(url: str) -> str:
            version = os.getenv('EMAIL_LOGO_VERSION') or os.getenv('ASSET_VERSION')
            if not version and getattr(settings, 'DEBUG', False):
                import time as _t
                version = str(int(_t.time()))
            return f"{url}{'&' if '?' in url else '?'}v={version}" if version else url

        logo = getattr(settings, 'EMAIL_LOGO_URL', None)
        if logo and isinstance(logo, str) and logo.lower().startswith('http'):
            return _append_version(logo)
        # Fallback basé sur FRONTEND_URL
        frontend = getattr(settings, 'FRONTEND_URL', '') or getattr(settings, 'FRONTEND_BASE_URL', '')
        if isinstance(frontend, str) and frontend.lower().startswith('https://') and ('localhost' not in frontend and '127.0.0.1' not in frontend):
            return _append_version(frontend.rstrip('/') + '/Logo_bg.png')
        return _append_version('https://www.optitab.net/Logo_bg.png')
    
    @staticmethod
    def send_verification_code(user, code):
        """Envoi du code de vérification par email"""
        try:
            send_mail(
                subject='Code de vérification OptiTAB',
                message=f'Bonjour {user.first_name},\n\nVotre code de vérification est : {code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(f"Code de vérification envoyé à {user.email}")
            return True
        except Exception as e:
            logger.error(f"Erreur envoi email à {user.email}: {e}")
            return False

    @staticmethod
    def send_verification_link(user, verification_link):
        """Envoie un lien de vérification d'email."""
        first_name = (user.first_name or '').strip() or 'OptiTABien'
        plain_message = (
            f"Bonjour {first_name},\n\n"
            "Merci de confirmer votre adresse email OptiTAB.\n"
            "Cliquez sur le lien ci-dessous pour valider votre email :\n"
            f"{verification_link}\n\n"
            "Ce lien expire dans 24 heures.\n\n"
            "À très vite,\nL'équipe OptiTAB"
        )

        logo_url = EmailService._resolve_logo_url()
        html_message = f"""
            <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                <tr>
                  <td style="padding:24px 24px 0 24px;">
                    {f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block;margin-bottom:16px;"/>' if logo_url else ''}
                    <h1 style="margin:0 0 12px 0;font-size:22px;color:#111827;">Confirmez votre email</h1>
                    <p style="margin:0;color:#4b5563;font-size:15px;line-height:1.6;">
                      Bonjour {first_name},<br/>
                      Merci de confirmer votre adresse email pour sécuriser votre compte.
                    </p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:24px;">
                    <a href="{verification_link}" style="display:inline-block;background:#4f46e5;color:#ffffff;text-decoration:none;font-weight:600;padding:12px 24px;border-radius:10px;">
                      Confirmer mon email
                    </a>
                    <p style="margin:16px 0 0 0;color:#6b7280;font-size:13px;line-height:1.6;">
                      Ce lien est valable pendant 24 heures. Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur :
                    </p>
                    <p style="margin:12px 0 0 0;color:#2563eb;font-size:13px;word-break:break-all;">
                      <a href="{verification_link}" style="color:#2563eb;text-decoration:none;">{verification_link}</a>
                    </p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:16px 24px;background:#f3f4f6;color:#6b7280;font-size:12px;">
                    L'équipe OptiTAB<br/>
                    <a href="mailto:contact@optitab.net" style="color:#4f46e5;text-decoration:none;">contact@optitab.net</a>
                  </td>
                </tr>
              </table>
            </div>
        """.strip()

        try:
            email_message = EmailMultiAlternatives(
                subject='Confirmez votre email OptiTAB',
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email_message.attach_alternative(html_message, "text/html")
            email_message.send(fail_silently=False)
            logger.info(f"Lien de vérification envoyé à {user.email}")
            return True
        except Exception as e:
            logger.error(f"Erreur envoi lien de vérification à {user.email}: {e}")
            return False
    
    @staticmethod
    def send_email_change_link(user, new_email, verification_link):
        """Envoie un lien de confirmation pour changer d'adresse email."""
        display_name = (user.first_name or '').strip() or 'OptiTABien'
        plain_message = (
            f"Bonjour {display_name},\n\n"
            f"Vous avez demandé à remplacer votre adresse email OptiTAB par {new_email}.\n"
            "Cliquez sur le lien ci-dessous pour confirmer ce changement :\n"
            f"{verification_link}\n\n"
            "Ce lien expire dans 24 heures. Si vous n'êtes pas à l'origine de cette demande, ignorez cet email.\n\n"
            "À très vite,\nL'équipe OptiTAB"
        )
        logo_url = EmailService._resolve_logo_url()
        html_message = f"""
            <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                <tr>
                  <td style="padding:24px 24px 0 24px;">
                    {f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block;margin-bottom:16px;"/>' if logo_url else ''}
                    <h1 style="margin:0 0 12px 0;font-size:22px;color:#111827;">Confirmez votre nouvelle adresse email</h1>
                    <p style="margin:0;color:#4b5563;font-size:15px;line-height:1.6;">
                      Bonjour {display_name},<br/>
                      Cliquez sur le bouton ci-dessous pour confirmer votre nouvelle adresse email.
                    </p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:24px;">
                    <a href="{verification_link}" style="display:inline-block;background:#6366f1;color:#ffffff;text-decoration:none;font-weight:600;padding:12px 24px;border-radius:10px;">
                      Confirmer mon nouvel email
                    </a>
                    <p style="margin:16px 0 0 0;color:#6b7280;font-size:13px;line-height:1.6;">
                      Nouveau mail : <strong style="color:#111827;">{new_email}</strong><br/>
                      Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur :
                    </p>
                    <p style="margin:12px 0 0 0;color:#2563eb;font-size:13px;word-break:break-all;">
                      <a href="{verification_link}" style="color:#2563eb;text-decoration:none;">{verification_link}</a>
                    </p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:16px 24px;background:#f3f4f6;color:#6b7280;font-size:12px;">
                    Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet email.
                  </td>
                </tr>
              </table>
            </div>
        """.strip()

        try:
            email_message = EmailMultiAlternatives(
                subject='Confirmation de changement d\'email OptiTAB',
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[new_email],
            )
            email_message.attach_alternative(html_message, "text/html")
            email_message.send(fail_silently=False)
            logger.info("Lien de changement d'email envoyé à %s", new_email)
            return True
        except Exception as e:
            logger.error("Erreur envoi lien de changement d'email à %s: %s", new_email, e)
            return False
    
    @staticmethod
    def send_password_reset(user, reset_link):
        """Envoi du lien de réinitialisation de mot de passe"""
        try:
            send_mail(
                subject='Réinitialisation de votre mot de passe OptiTAB',
                message=f'Bonjour {user.first_name},\n\nCliquez sur ce lien pour réinitialiser votre mot de passe : {reset_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(f"Lien de réinitialisation envoyé à {user.email}")
            return True
        except Exception as e:
            logger.error(f"Erreur envoi lien réinitialisation à {user.email}: {e}")
            return False

    @staticmethod
    def send_invoice_receipt(user, payment_history, invoice_link):
        """Envoie un email contenant la facture Stripe."""
        first_name = (user.first_name or '').strip() or 'OptiTABien'
        date_str = timezone.localtime(payment_history.created_at).strftime('%d %B %Y')
        amount_str = f"{payment_history.amount:.2f} {payment_history.currency.upper()}"
        subject = 'Votre facture OptiTAB'

        text_body = (
            f"Bonjour {first_name},\n\n"
            f"Voici la facture correspondant à votre paiement du {date_str} "
            f"d'un montant de {amount_str}.\n\n"
            f"Téléchargez-la en suivant ce lien sécurisé :\n{invoice_link}\n\n"
            "Merci pour votre confiance.\nL'équipe OptiTAB"
        )

        html_body = f"""
            <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                <tr>
                  <td style="padding:24px;">
                    <h1 style="margin:0 0 12px 0;font-size:20px;color:#111827;">Votre facture est disponible</h1>
                    <p style="margin:0 0 16px 0;color:#4b5563;font-size:15px;line-height:1.6;">
                      Bonjour {first_name},<br/>
                      Voici la facture correspondant à votre paiement du {date_str} (montant {amount_str}).
                    </p>
                    <a href="{invoice_link}" style="display:inline-block;background:#22c55e;color:#ffffff;text-decoration:none;font-weight:600;padding:12px 24px;border-radius:10px;">
                      Télécharger ma facture
                    </a>
                    <p style="margin:16px 0 0 0;color:#6b7280;font-size:13px;line-height:1.6;">
                      Si le bouton ne fonctionne pas, copiez ce lien dans votre navigateur :<br/>
                      <a href="{invoice_link}" style="color:#2563eb;text-decoration:none;">{invoice_link}</a>
                    </p>
                  </td>
                </tr>
              </table>
            </div>
        """

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=False)

    @staticmethod
    def send_contact_message(first_name: str, last_name: str, email: str, subject: str, message: str, ticket_id: str | None = None) -> bool:
        """Envoie un message du formulaire de contact vers la boîte de réception OptiTAB.

        Utilise Reply-To pour permettre la réponse directe à l'expéditeur.
        """
        try:
            to_email = os.getenv("CONTACT_RECIPIENT", "contact@optitab.net")
            # Sujet standardisé avec préfixe
            subject_prefix = os.getenv("CONTACT_SUBJECT_PREFIX", "[Contact OptiTAB]")
            ticket_part = f" [Ticket {ticket_id}]" if ticket_id else ""
            final_subject = f"{subject_prefix}{ticket_part} {subject.strip()}".strip()

            # Corps texte brut
            text_body = (
                f"Nouveau message depuis le formulaire de contact OptiTAB\n\n"
                f"Nom: {first_name.strip()} {last_name.strip()}\n"
                f"Email: {email.strip()}\n\n"
                f"Ticket: {ticket_id}\n\n" if ticket_id else ""
                f"Message:\n{message.strip()}\n"
            )

            # Variante HTML simple (avec logo si défini)
            logo_url = EmailService._resolve_logo_url()
            # Prépare le message en HTML (évite les backslashes dans les expressions d'f-strings)
            message_html = (message or '').strip().replace('\n', '<br/>')
            html_body = f"""
                <div>
                  {f'<p><img src="{logo_url}" alt="OptiTAB" style="height:64px;width:auto;display:block;-ms-interpolation-mode:bicubic"/></p>' if logo_url else ''}
                  <p><strong>Nouveau message depuis le formulaire de contact OptiTAB</strong></p>
                  {f'<p style="margin:6px 0 12px 0"><strong>Ticket:</strong> {ticket_id}</p>' if ticket_id else ''}
                  <p><strong>Nom:</strong> {first_name.strip()} {last_name.strip()}<br/>
                     <strong>Email:</strong> {email.strip()}</p>
                  <p><strong>Message:</strong><br/>{message_html}</p>
                  <hr style="border:none;border-top:1px solid #eee;margin:16px 0"/>
                  <table role="presentation" style="width:100%;max-width:520px;margin-top:16px">
                    <tr>
                      <td style="vertical-align:middle;padding-right:12px">
                        {f'<img src="{EmailService._resolve_logo_url()}" alt="OptiTAB" style="height:56px;width:auto;display:block"/>' if EmailService._resolve_logo_url() else ''}
                      </td>
                      <td style="vertical-align:middle;color:#6b7280;font-size:12px;line-height:1.5">
                        OptiTAB • Plateforme d'apprentissage<br/>
                        <a href="https://www.optitab.net" style="color:#6b7280;text-decoration:none">www.optitab.net</a> • contact@optitab.net
                      </td>
                    </tr>
                  </table>
                </div>
            """

            # Remise en forme professionnelle de l'email (gabarit carte)
            html_body = f"""
              <div style=\"background:#f3f4f6;padding:24px 0;\">
                <table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" style=\"width:100%;\">
                  <tr>
                    <td align=\"center\">
                      <table role=\"presentation\" width=\"600\" cellspacing=\"0\" cellpadding=\"0\" style=\"width:600px;max-width:100%;background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;\">
                        <tr>
                          <td style=\"padding:24px 24px 0 24px;\">{f'<img src="{logo_url}" alt="OptiTAB" style="height:64px;width:auto;display:block"/>' if logo_url else ''}</td>
                        </tr>
                        <tr>
                          <td style=\"padding:16px 24px 0 24px;\">
                            <h1 style=\"margin:0 0 6px 0;font-size:20px;line-height:1.3;color:#111827;\">Nouveau message de contact</h1>
                            <p style=\"margin:0;color:#6b7280;font-size:14px;\">Reçu via le formulaire OptiTAB.</p>
                          </td>
                        </tr>
                        <tr>
                          <td style=\"padding:16px 24px;\">
                            <table role=\"presentation\" width=\"100%\" style=\"font-size:14px;color:#111827;\">
                              <tr><td style=\"padding:6px 0;width:120px;color:#6b7280;\">Nom</td><td style=\"padding:6px 0;\">{first_name.strip()} {last_name.strip()}</td></tr>
                              <tr><td style=\"padding:6px 0;width:120px;color:#6b7280;\">Email</td><td style=\"padding:6px 0;\"><a href=\"mailto:{email.strip()}\" style=\"color:#4f46e5;text-decoration:none\">{email.strip()}</a></td></tr>
                              <tr><td style=\"padding:6px 0;width:120px;color:#6b7280;\">Sujet</td><td style=\"padding:6px 0;\">{subject.strip()}</td></tr>
                            </table>
                          </td>
                        </tr>
                        <tr>
                          <td style=\"padding:0 24px 16px 24px;\">
                            <div style=\"background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:16px;\">
                              <div style=\"font-weight:600;margin:0 0 8px 0;color:#111827;\">Message</div>
                              <div style=\"white-space:pre-wrap;line-height:1.6;color:#111827;\">{message_html}</div>
                            </div>
                          </td>
                        </tr>
                        <tr>
                          <td style=\"padding:0 24px 24px 24px;\">
                            <a href=\"mailto:{email.strip()}\" style=\"display:inline-block;background:#4f46e5;color:#ffffff;text-decoration:none;border-radius:8px;padding:10px 16px;font-weight:600;\">Répondre à {first_name.strip()}</a>
                          </td>
                        </tr>
                        <tr>
                          <td style=\"border-top:1px solid #e5e7eb;padding:16px 24px;color:#6b7280;font-size:12px;\">
                            <table role=\"presentation\" width=\"100%\">
                              <tr>
                                <td style=\"vertical-align:middle\">{f'<img src="{logo_url}" alt="OptiTAB" style="height:48px;width:auto;display:block"/>' if logo_url else ''}</td>
                                <td style=\"vertical-align:middle;text-align:right\">
                                  <span style=\"color:#374151;font-weight:600\">OptiTAB</span> • Plateforme d'apprentissage<br/>
                                  <a href=\"https://www.optitab.net\" style=\"color:#6b7280;text-decoration:none\">www.optitab.net</a> • contact@optitab.net
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </div>
            """

            email_msg = EmailMultiAlternatives(
                subject=final_subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email],
                reply_to=[email.strip()] if email else None,
            )
            email_msg.attach_alternative(html_body, "text/html")
            email_msg.send(fail_silently=False)
            logger.info("Message de contact envoyé à %s", to_email)
            return True
        except Exception as e:
            logger.error("Erreur lors de l'envoi du message de contact: %s", e)
            return False

    @staticmethod
    def send_contact_confirmation(to_email: str, first_name: str, subject: str, original_message: str = "", ticket_id: str | None = None) -> bool:
        """Envoie un email de confirmation à l'expéditeur du formulaire.

        Indique que le message a été reçu et que la réponse interviendra sous 24h.
        """
        try:
            display_name = (first_name or "").strip() or ""
            base_subject = os.getenv("CONTACT_CONFIRMATION_SUBJECT", "Nous avons bien reçu votre message - OptiTAB")
            ticket_part = f" [Ticket {ticket_id}]" if ticket_id else ""
            final_subject = f"{base_subject}{ticket_part}"

            text_body = (
                f"Bonjour {display_name},\n\n"
                f"Merci pour votre message. Nous l'avons bien reçu concernant \"{subject}\".\n"
                + (f"Numéro de ticket: {ticket_id}\n" if ticket_id else "") +
                f"Notre équipe vous répondra sous 24 heures (jours ouvrés).\n\n"
                f"Pour toute urgence, vous pouvez nous écrire à contact@optitab.net ou \n"
                f"nous joindre sur WhatsApp au 07 64 04 02 51.\n\n"
                f"Copie de votre message:\n{(original_message or '').strip()}\n\n"
                f"Cordialement,\nL'équipe OptiTAB\nhttps://www.optitab.net\n"
            )

            logo_url = EmailService._resolve_logo_url()
            original_html = (original_message or '').strip().replace('\n', '<br/>')
            html_body = f"""
                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#111">
                  {f'<p><img src="{logo_url}" alt="OptiTAB" style="height:64px;width:auto;display:block;-ms-interpolation-mode:bicubic"/></p>' if logo_url else ''}
                  <p>Bonjour {display_name},</p>
                  <p>Merci pour votre message. Nous l'avons bien reçu concernant <strong>{subject}</strong>.<br/>
                     Notre équipe vous répondra sous <strong>24 heures</strong> (jours ouvrés).</p>
                  {f'<p style="margin:6px 0 12px 0"><strong>Numéro de ticket:</strong> {ticket_id}</p>' if ticket_id else ''}
                  <p>Pour toute urgence, écrivez-nous à <a href="mailto:contact@optitab.net">contact@optitab.net</a>
                     ou contactez-nous sur WhatsApp au <a href="https://wa.me/33764040251" target="_blank">07 64 04 02 51</a>.</p>
                  <hr style="border:none;border-top:1px solid #eee;margin:16px 0"/>
                  <p style="margin:0 0 8px 0"><strong>Copie de votre message :</strong></p>
                  <p style="white-space:pre-wrap;margin:0">{original_html}</p>
                  <hr style="border:none;border-top:1px solid #eee;margin:16px 0"/>
                  <p style="color:#555">Cordialement,<br/>L'équipe OptiTAB<br/>
                     <a href="https://www.optitab.net">www.optitab.net</a></p>
                  <table role="presentation" style="width:100%;max-width:520px;margin-top:16px">
                    <tr>
                      <td style="vertical-align:middle;padding-right:12px">
                        {f'<img src="{EmailService._resolve_logo_url()}" alt="OptiTAB" style="height:56px;width:auto;display:block"/>' if EmailService._resolve_logo_url() else ''}
                      </td>
                      <td style="vertical-align:middle;color:#6b7280;font-size:12px;line-height:1.5">
                        OptiTAB • Plateforme d'apprentissage<br/>
                        <a href="https://www.optitab.net" style="color:#6b7280;text-decoration:none">www.optitab.net</a> • contact@optitab.net
                      </td>
                    </tr>
                  </table>
                </div>
            """

            from_email = settings.DEFAULT_FROM_EMAIL
            reply_to = [os.getenv("CONTACT_RECIPIENT", "contact@optitab.net")]

            # Remise en forme professionnelle (gabarit carte) pour la confirmation
            html_body = f"""
              <div style=\"background:#f3f4f6;padding:24px 0;\">
                <table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" style=\"width:100%;\">
                  <tr>
                    <td align=\"center\">
                      <table role=\"presentation\" width=\"600\" cellspacing=\"0\" cellpadding=\"0\" style=\"width:600px;max-width:100%;background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;\">
                        <tr>
                          <td style=\"padding:24px 24px 0 24px;\">{f'<img src="{logo_url}" alt="OptiTAB" style="height:64px;width:auto;display:block"/>' if logo_url else ''}</td>
                        </tr>
                        <tr>
                          <td style=\"padding:16px 24px 0 24px;\">
                            <h1 style=\"margin:0 0 6px 0;font-size:20px;line-height:1.3;color:#111827;\">Nous avons bien reçu votre message</h1>
                            <p style=\"margin:0;color:#6b7280;font-size:14px;\">Sujet: <strong>{subject}</strong></p>
                          </td>
                        </tr>
                        <tr>
                          <td style=\"padding:16px 24px;\">
                            <p style=\"margin:0 0 12px 0;color:#111827;\">Bonjour {display_name},</p>
                            <p style=\"margin:0 0 12px 0;color:#111827;\">Merci pour votre message. Notre équipe vous répondra sous <strong>24 heures</strong> (jours ouvrés).</p>
                            <p style=\"margin:0 0 16px 0;color:#6b7280;\">Pour urgence, écrivez-nous à <a href=\"mailto:contact@optitab.net\" style=\"color:#4f46e5;text-decoration:none\">contact@optitab.net</a> ou sur WhatsApp: <a href=\"https://wa.me/33764040251\" style=\"color:#4f46e5;text-decoration:none\">07 64 04 02 51</a>.</p>
                            <div style=\"background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:16px;\">
                              <div style=\"font-weight:600;margin:0 0 8px 0;color:#111827;\">Copie de votre message</div>
                              <div style=\"white-space:pre-wrap;line-height:1.6;color:#111827;\">{original_html}</div>
                            </div>
                          </td>
                        </tr>
                        <tr>
                          <td style=\"border-top:1px solid #e5e7eb;padding:16px 24px;color:#6b7280;font-size:12px;\">
                            <table role=\"presentation\" width=\"100%\">
                              <tr>
                                <td style=\"vertical-align:middle\">{f'<img src="{logo_url}" alt="OptiTAB" style="height:48px;width:auto;display:block"/>' if logo_url else ''}</td>
                                <td style=\"vertical-align:middle;text-align:right\">
                                  <span style=\"color:#374151;font-weight:600\">OptiTAB</span> • Plateforme d'apprentissage<br/>
                                  <a href=\"https://www.optitab.net\" style=\"color:#6b7280;text-decoration:none\">www.optitab.net</a> • contact@optitab.net
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </div>
            """

            email_msg = EmailMultiAlternatives(
                subject=final_subject,
                body=text_body,
                from_email=from_email,
                to=[to_email],
                reply_to=reply_to,
            )
            email_msg.attach_alternative(html_body, "text/html")
            email_msg.send(fail_silently=False)
            logger.info("Email de confirmation envoyé à %s", to_email)
            return True
        except Exception as e:
            logger.error("Erreur lors de l'envoi de l'email de confirmation: %s", e)
            return False

    @staticmethod
    def send_newsletter_welcome(subscriber, unsubscribe_url: str) -> bool:
        """Envoie un email de bienvenue avec lien de désinscription.

        - `subscriber`: instance avec attributs `.email`, `.first_name`
        - `unsubscribe_url`: URL absolue de désinscription (GET)
        """
        try:
            to_email = getattr(subscriber, 'email', None) or ''
            if not to_email:
                return False
            display_name = (getattr(subscriber, 'first_name', '') or '').strip() or 'cher membre'
            logo_url = EmailService._resolve_logo_url()

            subject = 'Bienvenue dans la newsletter OptiTAB'
            text_body = (
                f"Bonjour {display_name},\n\n"
                "Merci pour votre inscription à la newsletter OptiTAB. "
                "Vous recevrez régulièrement des nouveautés, des conseils et des ressources pour progresser en maths.\n\n"
                f"Pour vous désabonner à tout moment, cliquez ici : {unsubscribe_url}\n\n"
                "Cordialement,\nL'équipe OptiTAB\nwww.optitab.net"
            )

            html_body = f"""
                <div style="background:#f3f4f6;padding:24px">
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:600px;margin:auto;background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;overflow:hidden">
                    <tr>
                      <td style="padding:20px 24px 0 24px">{f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block"/>' if logo_url else ''}</td>
                    </tr>
                    <tr>
                      <td style="padding:6px 24px 0 24px">
                        <h1 style="margin:0 0 8px 0;font-size:20px;line-height:1.4;color:#111827">Bienvenue dans la newsletter OptiTAB</h1>
                        <p style="margin:0;color:#6b7280;font-size:14px">Ressources, nouveautés et conseils pour progresser en maths.</p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:16px 24px 8px 24px;color:#111827">
                        <p style="margin:0 0 12px 0">Bonjour {display_name},</p>
                        <p style="margin:0 0 12px 0">Merci pour votre inscription. Nous vous enverrons régulièrement des emails utiles et sans spam.</p>
                        <p style="margin:0 0 16px 0;color:#6b7280">Vous pouvez vous désabonner à tout moment en un clic.</p>
                        <p style="margin:0 0 24px 0">
                          <a href="{unsubscribe_url}" style="background:#2a38b7;color:#fff;text-decoration:none;padding:12px 18px;border-radius:8px;display:inline-block">Se désabonner</a>
                        </p>
                      </td>
                    </tr>
                    <tr>
                      <td style="border-top:1px solid #e5e7eb;padding:16px 24px;color:#6b7280;font-size:12px">
                        Cet email vous a été envoyé par OptiTAB. 
                        <a href="{unsubscribe_url}" style="color:#4f46e5;text-decoration:none">Se désabonner</a>
                      </td>
                    </tr>
                  </table>
                </div>
            """

            email_msg = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email],
            )
            email_msg.attach_alternative(html_body, "text/html")
            email_msg.send(fail_silently=False)
            logger.info("Email newsletter de bienvenue envoyé à %s", to_email)
            return True
        except Exception as e:
            logger.error("Erreur envoi email newsletter: %s", e)
            return False

    @staticmethod
    def render_newsletter_template(subject: str, content_html: str, unsubscribe_url: str) -> str:
        """Construit un HTML d'email avec entête (logo) et pied de page (désabonnement).

        - subject: titre affiché en tête du contenu
        - content_html: contenu HTML déjà sûr
        - unsubscribe_url: lien de désabonnement à inclure
        """
        logo_url = EmailService._resolve_logo_url()
        safe_subject = (subject or '').strip() or 'Newsletter OptiTAB'
        body_html = content_html or ''
        return f"""
          <div style=\"background:#f3f4f6;padding:24px 0;\">
            <table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" style=\"width:100%;\">
              <tr>
                <td align=\"center\">
                  <table role=\"presentation\" width=\"600\" cellspacing=\"0\" cellpadding=\"0\" style=\"width:600px;max-width:100%;background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;\">
                    <tr>
                      <td style=\"padding:20px 24px 0 24px;\">{f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block"/>' if logo_url else ''}</td>
                    </tr>
                    <tr>
                      <td style=\"padding:6px 24px 8px 24px;\">
                        <h1 style=\"margin:0 0 10px 0;font-size:20px;line-height:1.4;color:#111827\">{safe_subject}</h1>
                      </td>
                    </tr>
                    <tr>
                      <td style=\"padding:8px 24px 16px 24px;color:#111827;font-size:14px;line-height:1.6\">
                        {body_html}
                      </td>
                    </tr>
                    <tr>
                      <td style=\"border-top:1px solid #e5e7eb;padding:16px 24px;color:#6b7280;font-size:12px\">
                        Cet email vous a été envoyé par OptiTAB.
                        <a href=\"{unsubscribe_url}\" style=\"color:#4f46e5;text-decoration:none\">Se désabonner</a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </div>
        """


class ValidationService:
    """Service de validation réutilisable"""
    
    @staticmethod
    def generate_verification_code():
        """Génère un code de vérification à 6 chiffres"""
        return str(random.randint(100000, 999999))
    
    @staticmethod
    def validate_password_match(password1, password2):
        """Valide que les deux mots de passe correspondent"""
        if password1 != password2:
            raise ValueError("Les deux mots de passe ne correspondent pas")
        return True


class ResponseService:
    """Service pour standardiser les réponses API"""
    
    @staticmethod
    def success(message="Opération réussie", data=None, status_code=status.HTTP_200_OK):
        """Réponse de succès standardisée"""
        response_data = {"message": message, "success": True}
        if data is not None:
            response_data["data"] = data
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error(message="Une erreur s'est produite", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """Réponse d'erreur standardisée"""
        response_data = {"message": message, "success": False}
        if errors is not None:
            response_data["errors"] = errors
        return Response(response_data, status=status_code)
    
    @staticmethod
    def validation_error(errors):
        """Réponse d'erreur de validation standardisée"""
        return ResponseService.error(
            message="Erreurs de validation", 
            errors=errors, 
            status_code=status.HTTP_400_BAD_REQUEST
        )


class QuerySetService:
    """Service pour optimiser les requêtes en base"""
    
    @staticmethod
    def get_user_queryset():
        """QuerySet optimisé pour les utilisateurs avec leurs relations"""
        from users.models import CustomUser
        return CustomUser.objects.select_related('pays', 'niveau_pays')
    
    @staticmethod
    def get_curriculum_queryset():
        """QuerySet optimisé pour le curriculum avec toutes les relations"""
        from curriculum.models import Matiere
        # Chapitres supprimés → précharger directement via Notion
        return (
            Matiere.objects
            .select_related('niveau__pays')
            .prefetch_related(
                'themes__notions__exercices',
                'themes__notions__cours',
                'themes__notions__quiz',
            )
        )


class BaseQuerySet(models.QuerySet):
    """QuerySet de base avec méthodes communes"""
    
    def active(self):
        """Filtre les éléments actifs"""
        return self.filter(est_actif=True)
    
    def by_ordre(self):
        """Tri par ordre puis nom/titre"""
        if hasattr(self.model, 'titre'):
            return self.order_by('ordre', 'titre')
        elif hasattr(self.model, 'nom'):
            return self.order_by('ordre', 'nom')
        return self.order_by('ordre')


class BaseManager(models.Manager):
    """Manager de base avec méthodes communes"""
    
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)
    
    def active(self):
        """Retourne seulement les éléments actifs"""
        return self.get_queryset().active()
    
    def ordered(self):
        """Retourne les éléments triés par ordre"""
        return self.get_queryset().by_ordre()
    
    def active_ordered(self):
        """Retourne les éléments actifs triés par ordre"""
        return self.active().by_ordre()
